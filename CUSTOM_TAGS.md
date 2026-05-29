# Call Logs Custom Tag – Functional Requirement

## Overview

We need to create a **Call Logs Custom Tag** that will be inserted into the **Xibo CMS Display Name Row**.

This custom tag will allow users to:

* Save call-related information into a MySQL database
* View previously saved call history records
* Associate all records with a specific Display Name

---

# UI Design

## Single Row Form

### Input Fields

| Field              | Type                        | Validation | Notes                                                                       | 
| ------------------ | --------------------------  | ---------- | ----------------------------------------------------------------------------|
| Display Name       | Searchable Select Dropdown  | Required   | Values will be fetched from a different database using an external API call |
| Name               | Text Input                  | Required   | Customer/User Name                                                          |
| Phone Number       | Text Input                  | Required   | Customer Phone Number                                                       |
| Issue Type         | Dropdown                    | Required   | Predefined “Known Issues” will be hardcoded                                 |
| Add New Issue Type | Optional Input              | Optional   | If issue type is not available, user can add a new issue                    |
| Issue Description  | Text Area                   | Required   | Detailed issue description                                                  |
| Save Button        | Action Button               | -          | Saves data into MySQL DB with timestamp                                     |

---

# Issue Type Behavior

## Default Behavior

* Known Issues will be available in the dropdown by default.

## Dynamic Add Behavior

If the required issue is not available:

1. User can add a new issue type
2. Newly added issue type will be:

   * Stored in MySQL DB
   * Automatically available in the dropdown for future selections

---

# Save Operation

On clicking **Save Button**:

* Validate all required fields
* Save record into MySQL DB
* Store current timestamp
* Associate record with selected Display Name

---

# Database Fields

## Call Logs Table

| Column Name       | Type                              |
| ----------------- | --------------------------------- |
| id                | INT (Primary Key, Auto Increment) |
| display_name      | VARCHAR                           |
| call_log          | JSON                              |
| timestamp         | TiMEDATE                          |

---

## Issue Types Table

| Column Name | Type                              |
| ----------- | --------------------------------- |
| id          | INT (Primary Key, Auto Increment) |
| issue_name  | VARCHAR                           |
| created_at  | TIMESTAMP                         |

---

# Actions

## Call History Button

A “Call History” action/button should be available.

---

# Call History Modal

## Functionality

When user clicks **Call History**:

* Open modal popup
* Show all previously saved calls for the selected Display Name
* View-only access

## Modal Fields

| Field             |
| ----------------- |
| Customer Name     |
| Phone Number      |
| Issue Type        |
| Issue Description |
| Timestamp         |

---

# Important Condition

Since this custom tag will be inserted inside the **Xibo CMS Display Name Row**:

* The selected Display Name context is already known
* Therefore, the **Call History Modal should NOT contain the Display Name dropdown**
* History should automatically load based on the current Display Name row context

---

# API Requirements

## External API

Used for:

* Fetching searchable Display Name list

## Internal APIs Needed

### Save Call Log

POST `/api/call-logs/save`

### Fetch Call History

GET `/api/call-logs/history/{displayId}`

### Fetch Issue Types

GET `/api/issue-types`

### Add New Issue Type

POST `/api/issue-types/add`

---

# Expected Flow

1. User opens Xibo CMS row
2. Custom tag loads with current Display Name context
3. User fills:

   * Name
   * Phone Number
   * Issue Type
   * Issue Description
4. User clicks Save
5. Data stored in MySQL with timestamp
6. User clicks Call History
7. Modal opens showing all previous records for that Display Name


# UI Prototype Design:

```HTML

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Call Logs Custom Tag Prototype</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        .call-logs-container {
            padding: 20px;
            border: 1px solid #ccc;
            margin: 20px;
            border-radius: 5px;
        }

        .call-logs-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }

        .call-logs-title {
            margin: 0;
        }

        .call-logs-button {
            align-self: flex-end;
        }

        .call-logs-table {
            width: 100%;
            border-collapse: collapse;
        }

        .call-logs-table th, .call-logs-table td {
            border: 1px solid #ccc;
            padding: 10px;
            text-align: center;
        }

        .call-history-modal {
            display: none; /* Hidden by default */
            position: fixed; /* Stay in place */
            z-index: 1; /* Sit on top */
            left: 0;
            top: 0;
            width: 100%; /* Full width */
            height: 100%; /* Full height */
            overflow: auto; /* Enable scroll if needed */
            background-color: rgb(0,0,0); /* Fallback color */
            background-color: rgba(0,0,0,0.4); /* Black w/ opacity */
        }

        /* Modal Content/Box */
        .modal-content {
            background-color: #fefefe;
            margin: 15% auto; /* 15% from the top and centered */
            padding: 20px;
            border: 1px solid #888;
            width: 80%; /* Could be more or less, depending on screen size */
        }

        .call-history-header {
            margin-bottom: 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .call-history-title {
            margin: 0;
        }

        .call-history-close {
            color: #aaa;
            float: right;
            font-size: 28px;
            font-weight: bold;
        }

        .call-history-close:hover,
        .call-history-close:focus {
            color: black;
            text-decoration: none;
            cursor: pointer;
        }

        .call-history-body {
            max-height: 300px;
            overflow-y: auto;
            align-self: flex-end;
        }

    </style>
</head>
<body>
    <call-logs display-id="123" display-name="Test Tv AIPL"></call-logs>
    <script>
        // This is a prototype for a custom tag called <call-logs></call-logs>
        class CallLogs extends HTMLElement {
            connectedCallback() {

                const displayId = this.getAttribute('display-id');

                const displayName = this.getAttribute('display-name');

                const callLogsData = [
                    {
                        callerName: 'John Doe',
                        callerNumber: '123-456-7890',
                        issueType: 'Network Issue',
                        network: 'Wi-Fi (Wireless Router)',
                        description: 'Internet not working',
                        dateTime: '2024-06-01 10:00 AM'
                    },
                    {
                        callerName: 'Jane Smith',
                        callerNumber: '987-654-3210',
                        issueType: 'Billing Issue',
                        network: 'Ethernet (Wired)',
                        description: 'Incorrect bill amount',
                        dateTime: '2024-06-02 02:30 PM'
                    }
                ];

                this.innerHTML = `
                    <div class="call-logs-container">
                        <div class="call-logs-header">
                            <h3 class="call-logs-title">${displayName}</h3>
                            <button class="call-logs-button" id="callHistoryBtn">Call History</button>
                        </div>
                        <div>
                            <table class="call-logs-table">
                                <thead>
                                    <tr>
                                        <th>Caller Name</th>
                                        <th>Caller Number</th>
                                        <th>Issue Type</th>
                                        <th>Network</th>
                                        <th>Description</th>
                                        <th>Actions</th>
                                    </tr>
                                </thead>
                                <tbody class="call-logs-body">
                                    <tr>
                                        <td><input type="text" placeholder="Caller Name"/></td>
                                        <td><input type="text" placeholder="Caller Number"/></td>
                                        <td>
                                            <select>
                                                <option>Network Issue</option>
                                                <option>Billing Issue</option>
                                                <option>Technical Support</option>
                                            </select>
                                        </td>
                                        <td>
                                            <select>
                                                <option>Dongle</option>
                                                <option>Ethernet (Wired)</option>
                                                <option>Wi-Fi (Wireless Router)</option>
                                                <option>Others</option>
                                            </select>
                                        </td>
                                        <td><textarea placeholder="Description"></textarea></td>
                                        <td>
                                            <button>Save</button>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>

                        <div id="callHistoryModal" class="call-history-modal">
                            <div class="modal-content">
                                <div class="call-history-header">
                                    <h3 class="call-history-title">Call History <span style="font-size: 14px; color: #666;">(Recent 5 Calls)</span></h3>
                                    <span class="call-history-close">&times;</span>
                                </div>
                                <div>
                                    <table class="call-logs-table">
                                        <thead>
                                            <tr>
                                                <th>Caller Name</th>
                                                <th>Caller Number</th>
                                                <th>Issue Type</th>
                                                <th>Network</th>
                                                <th>Description</th>
                                                <th>Date & Time</th>
                                            </tr>
                                        </thead>
                                        <tbody class="call-history-body">
                                            <!-- Call history data will be populated here -->
                                            ${callLogsData.map(log => `
                                                <tr>
                                                    <td>${log.callerName}</td>
                                                    <td>${log.callerNumber}</td>
                                                    <td>${log.issueType}</td>
                                                    <td>${log.network}</td>
                                                    <td>${log.description}</td>
                                                    <td>${log.dateTime}</td>
                                                </tr>
                                            `).join('')}
                                        </tbody>
                                    </table>
                                </div>
                            </div>
                        </div>
                    </div>
                `;
            }
        }

        customElements.define('call-logs', CallLogs);

        // Get the Modal
        let modal = document.getElementById("callHistoryModal");

        // Get the button that opens the modal
        let btn = document.getElementById("callHistoryBtn");

        // Get the <span> element that closes the modal
        let span = document.getElementsByClassName("call-history-close")[0];

        // When the user clicks on <span> (x), close the modal
        btn.onclick = function() {
            modal.style.display = "block";
        }
        
        // When the user clicks on <span> (x), close the modal
        span.onclick = function() {
            modal.style.display = "none";
        }

        // When the user clicks anywhere outside of the modal, close it
        window.onclick = function(event) {
            if (event.target == modal) {
                modal.style.display = "none";
            }
        }

    </script>
</body>
</html>

```
