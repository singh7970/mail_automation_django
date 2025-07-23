from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.core.mail import EmailMessage, BadHeaderError
from django.conf import settings
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone


from app.models import Subscription
import csv
import openpyxl
import os
import urllib.parse
import pymysql
import psycopg2
import re
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition



from django.utils import timezone
from django.contrib import messages
from django.shortcuts import render, redirect
from django.core.mail import EmailMessage, BadHeaderError
from django.conf import settings
from django.contrib.auth.decorators import login_required

import csv, os, re, urllib
import pymysql, psycopg2
import openpyxl

from django.core.files.storage import FileSystemStorage
from app.models import Subscription, Register

@login_required(login_url='/')
def index(request):
    user = request.user

    # Check for active paid subscription
    has_access = Subscription.objects.filter(user=user, is_active=True).exists()

    # Check if user has Free Trial
    free_trial = Subscription.objects.filter(user=user, plan='Free Trial', is_active=True).first()

    # If free trial expired
    if free_trial and free_trial.end_date and free_trial.end_date < timezone.now():
        free_trial.is_active = False
        free_trial.save()
        has_access = False

    if request.method == 'POST':
        if not has_access:
            messages.error(request, "Your subscription is inactive. Please subscribe to use this feature.")
            return redirect('index')

        emails = []
        email_body = request.POST.get('emailBody')
        subject_line = request.POST.get('subject_line')
        sender_email = request.POST.get('sender_email')
        email_source = request.POST.get('email_source')

        uploaded_file = request.FILES.get('fileUpload')
        attachments = request.FILES.getlist('attachments')
        sql_url = request.POST.get('sql_url', '').strip()
        table_name = request.POST.get('table_name', '').strip()

        if not email_body or not subject_line or not sender_email:
            messages.error(request, "All fields are required.")
            return redirect('index')

        try:
            if email_source == 'csv':
                if not uploaded_file:
                    messages.error(request, "Please upload a CSV or Excel file.")
                    return redirect('index')

                fs = FileSystemStorage()
                filename = fs.save(uploaded_file.name, uploaded_file)
                file_path = fs.path(filename)

                if filename.endswith('.csv'):
                    with open(file_path, newline='', encoding='utf-8') as f:
                        reader = csv.reader(f)
                        for row in reader:
                            if row and '@' in row[0]:
                                emails.append(row[0])
                elif filename.endswith(('.xlsx', '.xls')):
                    wb = openpyxl.load_workbook(file_path, read_only=True)
                    sheet = wb.active
                    for row in sheet.iter_rows(min_row=1, values_only=True):
                        if row and row[0] and '@' in str(row[0]):
                            emails.append(str(row[0]))
                    wb.close()
                else:
                    messages.error(request, "Unsupported file type.")
                    return redirect('index')

                if os.path.exists(file_path):
                    os.remove(file_path)

            elif email_source == 'sql':
                if not sql_url or not table_name:
                    messages.error(request, "Please provide both SQL URL and Table Name.")
                    return redirect('index')

                parsed = urllib.parse.urlparse(sql_url)
                engine = parsed.scheme
                user_db = parsed.username
                password = urllib.parse.unquote(parsed.password)
                host = parsed.hostname
                port = parsed.port
                db_name = parsed.path[1:]

                if engine == 'mysql':
                    conn = pymysql.connect(host=host, port=port, user=user_db, password=password, db=db_name)
                elif engine == 'postgres':
                    conn = psycopg2.connect(host=host, port=port, user=user_db, password=password, dbname=db_name)
                else:
                    messages.error(request, "Unsupported DB engine.")
                    return redirect('index')

                cursor = conn.cursor()
                cursor.execute(f"SELECT email FROM {table_name}")
                rows = cursor.fetchall()
                emails = [row[0] for row in rows if re.match(r"[^@]+@[^@]+\.[^@]+", str(row[0]))]
                cursor.close()
                conn.close()
            else:
                messages.error(request, "Invalid email source selected.")
                return redirect('index')

        except Exception as e:
            messages.error(request, f"Error fetching emails: {str(e)}")
            return redirect('index')

        try:
            if emails:
                email = EmailMessage(
                    subject=subject_line,
                    body=email_body,
                    from_email=settings.EMAIL_HOST_USER,
                    to=emails,
                )
                for f in attachments:
                    email.attach(f.name, f.read(), f.content_type)
                email.send(fail_silently=False)
                messages.success(request, f"Campaign sent to {len(emails)} recipients.")

                # ✅ Deactivate Free Trial after first send
                if free_trial:
                    free_trial.is_active = False
                    free_trial.end_date = timezone.now()
                    free_trial.save()

                    # Mark user trial as used
                    user.has_used_trial = True
                    user.save()

                    # Update has_access to False for immediate effect
                    has_access = False

            else:
                messages.warning(request, "No valid email addresses found.")
        except BadHeaderError:
            messages.error(request, "Invalid email header.")
        except Exception as e:
            messages.error(request, f"Email sending failed: {str(e)}")

        return redirect('index')

    return render(request, 'index.html', {'has_access': has_access})



# API View (unchanged)
def fetch_emails_api(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST method allowed.'}, status=405)

    sql_url = request.POST.get('sql_url')
    table_name = request.POST.get('table_name')

    if not sql_url or not table_name:
        return JsonResponse({'error': 'sql_url and table_name are required.'}, status=400)

    try:
        parsed = urllib.parse.urlparse(sql_url)
        engine = parsed.scheme
        user = parsed.username
        password = urllib.parse.unquote(parsed.password)
        host = parsed.hostname
        port = parsed.port
        db_name = parsed.path[1:]

        if engine == 'mysql':
            conn = pymysql.connect(
                host=host, port=port, user=user, password=password, db=db_name
            )
        elif engine == 'postgres':
            conn = psycopg2.connect(
                host=host, port=port, user=user, password=password, dbname=db_name
            )
        else:
            return JsonResponse({'error': 'Unsupported engine. Use mysql or postgres.'}, status=400)

        cursor = conn.cursor()
        cursor.execute(f"SELECT email FROM {table_name}")
        rows = cursor.fetchall()
        emails = [row[0] for row in rows if re.match(r"[^@]+@[^@]+\.[^@]+", str(row[0]))]
        cursor.close()
        conn.close()

        return JsonResponse({'emails': emails, 'count': len(emails)})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)











