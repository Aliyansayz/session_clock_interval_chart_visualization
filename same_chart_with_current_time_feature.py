<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Forex Market Time Zone Converter</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f4; /* Light background for better contrast */
        }
        #canvas-container {
            position: relative;
            width: 80%; /* Adjusted width for flags and names */
            height: 400px;
            border: 1px solid #ddd;
            margin-left: 150px; /* Space for flags and names */
            background-color: white; /* White background for the container */
            border-radius: 10px; /* Rounded corners */
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1); /* Subtle shadow */
        }
        .session-rect {
            position: absolute;
            height: 40px;
            border-radius: 5px;
        }
        .session-rect.australia {
            background-color: #3a80f6;
        }
        .session-rect.usa {
            background-color: #34c759;
        }
        .session-rect.uk {
            background-color: #1e90ff;
        }
        .session-rect.japan {
            background-color: #ff6347;
        }
        /* X-axis scale between 1 to 24 */
        .x-axis {
            position: absolute;
            bottom: 0;
            left: 0;
            width: 100%;
            height: 30px;
            display: flex;
            justify-content: space-between;
        }

        /* Styling the flags and country names */
        .flag-container {
            position: absolute;
            display: flex;
            align-items: center;
            left: -150px; /* Positioning flags and names to the left */
        }
        .flag-container img {
            width: 24px;
            height: 24px;
            margin-right: 10px;
        }

        /* Current time placeholder */
        #current-time {
            position: absolute;
            top: 10px; /* Position above the canvas */
            left: 50%; /* Center it horizontally */
            transform: translateX(-50%);
            font-size: 24px;
            font-weight: bold;
            color: purple; /* Purple text for current time */
            background-color: rgba(255, 255, 255, 0.8); /* Slightly transparent background */
            padding: 5px 10px; /* Padding for better aesthetics */
            border-radius: 5px; /* Rounded corners */
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1); /* Subtle shadow */
        }

        /* Needle style */
        .needle {
            position: absolute;
            bottom: 40px; /* Above the X-axis */
            left: 50%; /* Center it horizontally */
            width: 0; /* No width, we use border for triangle */
            height: 0;
            border-left: 5px solid transparent;
            border-right: 5px solid transparent;
            border-bottom: 20px solid purple; /* Purple color for the needle */
            transform: translateX(-50%); /* Center it */
        }
    </style>
</head>
<body>

<div id="canvas-container">
    <div id="current-time">Current Time: <span id="time-display"></span></div>
    <div class="needle" id="needle"></div>
    <!-- Dynamic trading session bars and flag containers will be inserted here by JavaScript -->

    <!-- X-axis scale will be inserted here by JavaScript -->
    <div class="x-axis" id="x-axis"></div>
</div>

<script>
    // Data for each country and its session (start time, end time)
    const tradingSessions = [
        {
            name: "Australia",
            flag: "https://flagcdn.com/au.svg",
            startTime: 1,
            endTime: 10,
            nextDayReached: false,
            cssClass: "australia",
            topPosition: 50
        },
        {
            name: "USA",
            flag: "https://flagcdn.com/us.svg",
            startTime: 17,
            endTime: 2,
            nextDayReached: true,  // Crosses midnight
            cssClass: "usa",
            topPosition: 130
        },
        {
            name: "London, UK",
            flag: "https://flagcdn.com/gb.svg",
            startTime: 12,
            endTime: 18,
            nextDayReached: false,
            cssClass: "uk",
            topPosition: 210
        },
        {
            name: "Tokyo, Japan",
            flag: "https://flagcdn.com/jp.svg",
            startTime: 2,
            endTime: 8,
            nextDayReached: false,
            cssClass: "japan",
            topPosition: 290
        }
    ];

    const container = document.getElementById('canvas-container');
    const totalHours = 24; // Total hours in the X-axis scale
    const needle = document.getElementById('needle');
    const timeDisplay = document.getElementById('time-display');

    // Function to dynamically create the session bars and flag containers
    function createSessionBars() {
        tradingSessions.forEach(session => {
            if (session.nextDayReached) {
                // First bar: from startTime to 24 (midnight)
                const firstLeftPosition = (session.startTime / totalHours) * 100;
                const firstSessionWidth = ((24 - session.startTime) / totalHours) * 100;
                
                // Second bar: from 1 to endTime
                const secondLeftPosition = (0 / totalHours) * 100; // starts from 0% (1 a.m.)
                const secondSessionWidth = (session.endTime / totalHours) * 100;

                // Create first session div (bar before midnight)
                const firstSessionDiv = document.createElement('div');
                firstSessionDiv.classList.add('session-rect', session.cssClass);
                firstSessionDiv.style.left = `${firstLeftPosition}%`;
                firstSessionDiv.style.width = `${firstSessionWidth}%`;
                firstSessionDiv.style.top = `${session.topPosition}px`;

                // Create second session div (bar after midnight)
                const secondSessionDiv = document.createElement('div');
                secondSessionDiv.classList.add('session-rect', session.cssClass);
                secondSessionDiv.style.left = `${secondLeftPosition}%`;
                secondSessionDiv.style.width = `${secondSessionWidth}%`;
                secondSessionDiv.style.top = `${session.topPosition}px`;

                // Append both session divs
                container.appendChild(firstSessionDiv);
                container.appendChild(secondSessionDiv);
            } else {
                // Normal session: from startTime to endTime
                const leftPosition = (session.startTime / totalHours) * 100;
                const sessionWidth = ((session.endTime - session.startTime) / totalHours) * 100;

                // Create session div (bar)
                const sessionDiv = document.createElement('div');
                sessionDiv.classList.add('session-rect', session.cssClass);
                sessionDiv.style.left = `${leftPosition}%`;
                sessionDiv.style.width = `${sessionWidth}%`;
                sessionDiv.style.top = `${session.topPosition}px`;

                // Append session div
                container.appendChild(sessionDiv);
            }

            // Create flag and name container
            const flagDiv = document.createElement('div');
            flagDiv.classList.add('flag-container', session.cssClass);
            flagDiv.style.top = `${session.topPosition}px`; // Position it at the same Y level as the bar
            const flagImg = document.createElement('img');
            flagImg.src = session.flag;
            const countryName = document.createElement('span');
            countryName.innerText = session.name;

            // Append flag and name to the flagDiv
            flagDiv.appendChild(flagImg);
            flagDiv.appendChild(countryName);

            // Append flagDiv to the container
            container.appendChild(flagDiv);
        });
    }

    // Function to create X-axis labels dynamically
    function createXAxisLabels() {
        const xAxis = document.getElementById('x-axis');
        for (let i = 1; i <= totalHours; i++) {
            const labelDiv = document.createElement('div');
            labelDiv.innerText = i;
            xAxis.appendChild(labelDiv);
        }
    }

    // Function to update needle position based on current time
    function updateNeedlePosition() {
        const now = new Date();
        const currentHour = now.getHours();
        const currentMinute = now.getMinutes();
        
        // Calculate the needle position (in percentage) based on the current time
        const needlePosition = ((currentHour % 24) + currentMinute / 60) / totalHours * 100;
        needle.style.left = `${needlePosition}%`;

        // Update the time display
        timeDisplay.innerText = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    }

    // Initial call to create and display the session bars and X-axis
    createSessionBars();
    createXAxisLabels();
    
    // Initial position of the needle and current time display
    updateNeedlePosition();

    // Update the needle position and time every minute
    setInterval(updateNeedlePosition, 60000); // 60,000 ms = 1 minute
</script>

</body>
</html>
