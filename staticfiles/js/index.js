function showFileName() {
    const fileInput = document.getElementById("fileUpload");
    const fileNameDisplay = document.getElementById("file-name");
    if (fileInput.files.length > 0) {
      fileNameDisplay.textContent = `Selected file: ${fileInput.files[0].name}`;
    } else {
      fileNameDisplay.textContent = "";
    }
  }

  function updateAttachmentLabel() {
    const input = document.getElementById("attachmentInput");
    const label = document.getElementById("attachment-label");
    const files = input.files;
    if (files.length > 0) {
      const names = Array.from(files).map(file => file.name).join(", ");
      label.textContent = "Attachments: " + names;
    } else {
      label.textContent = "";
    }
  }

  function switchTab(tabName) {
    const contents = document.querySelectorAll(".tab-content");
    contents.forEach((content) => (content.style.display = "none"));

    const tabs = document.querySelectorAll(".tab");
    tabs.forEach((tab) => tab.classList.remove("active"));

    document.getElementById(tabName + "-content").style.display = "block";
    event.target.closest(".tab").classList.add("active");
  }

  document.getElementById("sms-message").addEventListener("input", function () {
    const remaining = 160 - this.value.length;
  });

  function getCSRFToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
  }

  function checkConnection() {
    const sqlUrl = document.getElementById('sql_url').value;
    const tableName = document.getElementById('table_name').value;
    const statusDiv = document.getElementById('sql-status');
    const resultDiv = document.getElementById('preview-results');

    if (!sqlUrl || !tableName) {
      alert("Please enter SQL URL and Table Name.");
      return;
    }

    statusDiv.innerText = "🔄 Checking connection...";
    resultDiv.innerHTML = "";

    fetch('/api/fetch-emails/', {
      method: 'POST',
      headers: {
        'X-CSRFToken': getCSRFToken(),
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      body: `sql_url=${encodeURIComponent(sqlUrl)}&table_name=${encodeURIComponent(tableName)}`
    })
    .then(response => response.json())
    .then(data => {
      if (data.emails) {
        statusDiv.innerText = `✅ Connection established. ${data.count} emails found.`;
      } else {
        statusDiv.innerText = `❌ ${data.error || 'Failed to connect.'}`;
      }
    })
    .catch(error => {
      statusDiv.innerText = `❌ Error: ${error}`;
    });
  }

  function previewEmails() {
    const sqlUrl = document.getElementById('sql_url').value;
    const tableName = document.getElementById('table_name').value;
    const statusDiv = document.getElementById('sql-status');
    const resultDiv = document.getElementById('preview-results');

    if (!sqlUrl || !tableName) {
      alert("Please enter SQL URL and Table Name.");
      return;
    }

    statusDiv.innerText = "🔄 Fetching emails...";
    resultDiv.innerHTML = "";

    fetch('/api/fetch-emails/', {
      method: 'POST',
      headers: {
        'X-CSRFToken': getCSRFToken(),
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      body: `sql_url=${encodeURIComponent(sqlUrl)}&table_name=${encodeURIComponent(tableName)}`
    })
    .then(response => response.json())
    .then(data => {
      if (data.emails) {
        statusDiv.innerText = `✅ Connection established. Showing ${data.count} emails.`;
        resultDiv.innerHTML = `<ul>${data.emails.slice(0, 10).map(email => `<li>${email}</li>`).join("")}</ul>`;
      } else {
        statusDiv.innerText = `❌ ${data.error || 'Failed to fetch.'}`;
      }
    })
    .catch(error => {
      statusDiv.innerText = `❌ Error: ${error}`;
    });
  }

  function toggleSource() {
  const selected = document.querySelector('input[name="email_source"]:checked').value;

  const csvBlock = document.getElementById("csv-block");
  const sqlBlock = document.getElementById("sql-block");

  csvBlock.style.display = selected === "csv" ? "block" : "none";
  sqlBlock.style.display = selected === "sql" ? "block" : "none";

  // Disable unused inputs
  document.getElementById("fileUpload").disabled = selected !== "csv";
  document.getElementById("sql_url").disabled = selected !== "sql";
  document.getElementById("table_name").disabled = selected !== "sql";
}


 function validateForm() {
  const selected = document.querySelector('input[name="email_source"]:checked').value;

  const fileInput = document.getElementById("fileUpload");
  const sqlUrl = document.getElementById("sql_url").value.trim();
  const tableName = document.getElementById("table_name").value.trim();

  const campaignName = document.getElementById("campaign-name").value.trim();
  const subjectLine = document.getElementById("subject-line").value.trim();
  const emailBody = document.getElementById("email-message").value.trim();
  const senderEmail = document.getElementById("sender-email").value.trim();

  if (!campaignName || !subjectLine || !emailBody || !senderEmail) {
    alert("Please fill in all required fields.");
    return false;
  }

  if (selected === "csv") {
    if (!fileInput || !fileInput.files.length) {
      alert("Please upload a CSV or Excel file.");
      return false;
    }
  } else if (selected === "sql") {
    if (!sqlUrl || !tableName) {
      alert("Please provide both SQL URL and Table Name.");
      return false;
    }
  }

  return true; // Only allow form submission when valid
}

window.addEventListener("DOMContentLoaded", () => {
  toggleSource();
});



 function openAIModal() {
      document.getElementById("aiModal").style.display = "block";
    }

    function closeAIModal() {
      document.getElementById("aiModal").style.display = "none";
    }

function generateAIContent() {
  const prompt = document.getElementById("aiPrompt").value;
  if (!prompt.trim()) {
    alert("Please enter a prompt for AI.");
    return;
  }

  fetch("/api/ai-generate/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ prompt: prompt }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.content) {
        document.getElementById("email-message").value = data.content;
        closeAIModal();
      } else {
        alert("Failed to generate AI content: " + (data.error || "Unknown error"));
      }
    })
    .catch((error) => {
      console.error("Error:", error);
      alert("Error communicating with AI server.");
    });
}

    function updateAttachmentLabel() {
      const input = document.getElementById("attachmentInput");
      const label = document.getElementById("attachment-label");
      if (input.files.length > 0) {
        label.textContent = input.files.length + " file(s) selected";
      } else {
        label.textContent = "";
      }
    }

    function showFileName() {
      const fileInput = document.getElementById("fileUpload");
      const fileName = document.getElementById("file-name");
      if (fileInput.files.length > 0) {
        fileName.textContent = fileInput.files[0].name;
      } else {
        fileName.textContent = "";
      }
    }

    function toggleSource() {
      const csvBlock = document.getElementById("csv-block");
      const sqlBlock = document.getElementById("sql-block");
      const source = document.querySelector('input[name="email_source"]:checked').value;
      if (source === "csv") {
        csvBlock.style.display = "block";
        sqlBlock.style.display = "none";
      } else {
        csvBlock.style.display = "none";
        sqlBlock.style.display = "block";
      }
    }

    function getCSRFToken() {
  const cookieValue = document.cookie
    .split("; ")
    .find((row) => row.startsWith("csrftoken="))
    ?.split("=")[1];
  return cookieValue;
}
