# Call Logs Custom Web Component – Functional Requirement

## Overview

A reusable custom Web Component named:

```html
<call-logs></call-logs>
```

will be embedded inside each Display row in the Xibo CMS Display page.

The component will allow users to:

* Log support/customer calls against a Display
* Store call information in MySQL
* View recent call history for that Display
* Associate all records with the corresponding Display ID and Display Name

---

# Component Usage

The component will be rendered dynamically for each Xibo Display row.

Example:

```html
<call-logs
    display-id="123"
    display-name="Test TV AIPL">
</call-logs>
```

Attributes:

| Attribute    | Description                 |
| ------------ | --------------------------- |
| display-id   | Unique Display Identifier   |
| display-name | Human-readable Display Name |

The component should display the Display Name in the UI and use the Display ID internally for saving and fetching records.

---

# UI Design

## Call Log Entry Form

### Header Section

| Element             | Description                     |
| ------------------- | ------------------------------- |
| Display Name        | Current Display Name            |
| Call History Button | Opens recent call history modal |

Example:

```text
Test TV AIPL                              [Call History]
```

---

## Input Fields

| Field         | Type       | Validation |
| ------------- | ---------- | ---------- |
| Caller Name   | Text Input | Required   |
| Caller Number | Text Input | Required   |
| Issue Type    | Dropdown   | Required   |
| Network       | Dropdown   | Required   |
| Description   | Text Area  | Required   |
| Save          | Button     | Action     |

---

## Issue Type Options

Default values:

* Network Issue
* Billing Issue
* Technical Support

Future enhancement:

* Allow administrators to manage Issue Types through database configuration.

---

## Network Options

Default values:

* Dongle
* Ethernet (Wired)
* Wi-Fi (Wireless Router)
* Others

---

# Save Operation

When Save is clicked:

1. Validate required fields
2. Create payload
3. Store record in MySQL
4. Generate timestamp automatically
5. Associate record with current Display ID and Display Name

Example payload:

```json
{
  "displayId": 123,
  "displayName": "Test TV AIPL",
  "callerName": "John Doe",
  "callerNumber": "1234567890",
  "issueType": "Network Issue",
  "network": "Wi-Fi (Wireless Router)",
  "description": "Internet not working"
}
```

---

# Database Design

## Call Logs Table

| Column Name  | Type                     |
| ------------ | ------------------------ |
| id           | INT (PK, Auto Increment) |
| display_id   | VARCHAR                  |
| display_name | VARCHAR                  |
| call_log     | JSON                     |
| created_at   | TIMESTAMP                |

Example JSON:

```json
{
  "callerName": "John Doe",
  "callerNumber": "1234567890",
  "issueType": "Network Issue",
  "network": "Wi-Fi (Wireless Router)",
  "description": "Internet not working"
}
```

---

## Issue Types Table

| Column Name | Type                     |
| ----------- | ------------------------ |
| id          | INT (PK, Auto Increment) |
| issue_name  | VARCHAR                  |
| created_at  | TIMESTAMP                |

---

# Call History

## History Button

Each component instance should contain a Call History button.

Clicking the button opens a modal dialog.

---

## History Modal

### Behaviour

* Read-only
* Shows recent 5 records only
* Filtered automatically by Display ID
* No Display selector shown inside modal

### Columns

| Field         |
| ------------- |
| Caller Name   |
| Caller Number |
| Issue Type    |
| Network       |
| Description   |
| Date & Time   |

---

# Data Loading Strategy

## Initial Page Load

When the Xibo Display page loads:

1. Load Display data
2. Load recent call history data
3. Cache results in memory

Goal:

Avoid making additional API requests every time a user clicks Call History.

---

# API Requirements

## Save Call Log

```http
POST /api/call-logs/save
```

---

## Fetch Call History

```http
GET /api/call-logs/history/{displayId}
```

Returns latest 5 records.

---

## Fetch Issue Types

```http
GET /api/issue-types
```

---

# Component Requirements

The solution must be implemented as a reusable Web Component:

```html
<call-logs
    display-id="123"
    display-name="Test TV AIPL">
</call-logs>
```

Requirements:

* Multiple instances may exist on the same page
* Each instance manages its own form and modal
* Avoid global IDs
* Use component-scoped event handlers
* Display Name shown in UI
* Display ID used internally for save and fetch operations

---

# Expected User Flow

1. Xibo Display page loads
2. Display rows are rendered
3. A `<call-logs>` component is created for each Display
4. User enters:

   * Caller Name
   * Caller Number
   * Issue Type
   * Network
   * Description
5. User clicks Save
6. Record is stored against the Display ID
7. User clicks Call History
8. Modal opens
9. Recent 5 call records are displayed
10. User closes modal


# UI Prototype

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

# OR

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
                    <style>
                        .call-logs-container {
                            padding: 20px;
                            border: 1px solid #ccc;
                            margin: 20px;
                            border-radius: 5px;
                            font-family: Arial, sans-serif;
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
    
                        .call-logs-table {
                            width: 100%;
                            border-collapse: collapse;
                        }
    
                        .call-logs-table th,
                        .call-logs-table td {
                            border: 1px solid #ccc;
                            padding: 10px;
                            text-align: center;
                        }
    
                        .call-history-container {
                            margin-top: 20px;
                            border: 1px solid #ccc;
                            border-radius: 5px;
                            padding: 15px;
                            display: none;
                        }
    
                        .call-history-header {
                            margin-bottom: 15px;
                        }
    
                        .call-history-body {
                            max-height: 300px;
                            overflow-y: auto;
                        }
    
                        input,
                        select,
                        textarea {
                            width: 100%;
                            box-sizing: border-box;
                        }
    
                        textarea {
                            resize: vertical;
                        }
                    </style>
    
                    <div class="call-logs-container">
    
                        <div class="call-logs-header">
                            <h3 class="call-logs-title">${displayName}</h3>
    
                            <button class="call-logs-button">
                                Call History
                            </button>
                        </div>
    
                        <!-- Form Table -->
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
                                        <td>
                                            <input type="text" placeholder="Caller Name"/>
                                        </td>
    
                                        <td>
                                            <input type="text" placeholder="Caller Number"/>
                                        </td>
    
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
    
                                        <td>
                                            <textarea placeholder="Description"></textarea>
                                        </td>
    
                                        <td>
                                            <button>Save</button>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
    
                        <!-- Call History Section -->
                        <div class="call-history-container">
    
                            <div class="call-history-header">
                                <h3 class="call-history-title">
                                    Call History
                                    <span style="font-size: 14px; color: #666;">
                                        (Recent 5 Calls)
                                    </span>
                                </h3>
                            </div>
    
                            <div class="call-history-body">
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
    
                                    <tbody>
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
                `;
    
                // Toggle Call History
                const historyBtn = this.querySelector('.call-logs-button');
                const historyContainer = this.querySelector('.call-history-container');
    
                historyBtn.addEventListener('click', () => {
    
                    const isVisible =
                        historyContainer.style.display === 'block';
    
                    historyContainer.style.display =
                        isVisible ? 'none' : 'block';
                });
            }
        }
    
        customElements.define('call-logs', CallLogs);
    </script>
</body>
</html>

```
