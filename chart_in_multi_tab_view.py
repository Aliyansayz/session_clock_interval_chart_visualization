<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Forex Market Time Zone Converter</title>

	<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>    
    <style>
                body {
                    margin: 0;
                    padding: 0;
                    font-family: 'Arial', sans-serif;
                    background-color: #1e1e2d;
                    color: #ffffff;
                }
                .header {
                    display: flex;
                    justify-content: space-between;
                    padding: 20px;
                    background-color: #2a2d3e;
                }
                .tabs {
                    display: flex;
                    cursor: pointer;
                    margin: 20px;
                }
                .tab {
                    padding: 10px 20px;
                    border: 1px solid #444;
                    border-radius: 5px 5px 0 0;
                    background-color: #2a2d3e;
                    margin-right: 5px;
                }
                .tab.active {
                    background-color: #3e4451;
                }
                .content {
                    padding: 20px;
                    border: 1px solid #444;
                    border-radius: 0 0 5px 5px;
                    background-color: #2a2d3e;
                }
    
    
    
    
    
        body {
            font-family: Arial, sans-serif;
        }

        #canvas-container {
            position: relative;
            width: 80%;
            height: 400px;
            border: 1px solid #ddd;
            margin-left: 150px;
        }

        .session-rect {
            position: absolute;
            height: 40px;
            border-radius: 5px;
        }

        /* Define the specific session colors */
        .session-rect.australia {
            background-color: indigo;
        }

        .session-rect.usa {
            background-color: green;
        }

        .session-rect.uk {
            background-color: skyblue;
        }

        .session-rect.japan {
            background-color: violet;
        }

        /* Styling for the needle */
        .needle {
            position: absolute;
            width: 2px;
            height: 100%; /* Full height */
            background-color: purple;
            z-index: 10; /* To ensure it's above all other elements */
        }

        /* Placeholder for current time */
        .current-time-placeholder {
            position: absolute;
            top: 0;
            background-color: purple;
            color: white;
            padding: 5px;
            border-radius: 5px;
            font-size: 14px;
            text-align: center;
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
            left: -150px;
        }

        .flag-container img {
            width: 24px;
            height: 24px;
            margin-right: 10px;
        }
    </style>
</head>
<body>

<div class="header">
                <h1>Crypto Dashboard</h1>
            </div>

            <div class="tabs">
                <div class="tab active" data-tab="portfolio">Portfolio</div>
                <div class="tab" data-tab="funding">Funding</div>
                <div class="tab" data-tab="session_chart">Session Chart</div>
                <div class="tab" data-tab="market">Market Table</div>
            </div>

            <div class="content">
                <div id="portfolio" class="tab-content">
                    <h2>Your Portfolio</h2>
                    <p>Portfolio content goes here...</p>
                </div>
                <div id="funding" class="tab-content" style="display: none;">
                    <h2>Funding Options</h2>
                    <p>Funding options go here...</p>
                </div>
                <div id="session_chart" class="tab-content" style="display: none;">
                    <h2>Assets Overview</h2>
                    
                    <div id="canvas-container">
    <!-- Needle for current time -->
    <div class="needle" id="needle"></div>

    <!-- Placeholder for current time -->
    <div class="current-time-placeholder" id="current-time"></div>

    <!-- X-axis scale will be inserted here by JavaScript -->
    <div class="x-axis" id="x-axis"></div>
</div>


                    
                    <p>Assets overview goes here...</p>
                </div>

              </div>

<script>

$('.tab').click(function() {
                    var tabId = $(this).data('tab');
                    $('.tab').removeClass('active');
                    $(this).addClass('active');
                    $('.tab-content').hide();
                    $('#' + tabId).show();
                });

</script>

<script>



    const totalHours = 24; // Total hours in the X-axis scale
    const tradingSessions = [
        { name: "Australia", flag: "https://flagcdn.com/au.svg", startTime: 1, endTime: 10, nextDayReached: false, cssClass: "australia", topPosition: 50 },
        { name: "USA", flag: "https://flagcdn.com/us.svg", startTime: 17, endTime: 2, nextDayReached: true, cssClass: "usa", topPosition: 130 },
        { name: "London, UK", flag: "https://flagcdn.com/gb.svg", startTime: 12, endTime: 18, nextDayReached: false, cssClass: "uk", topPosition: 210 },
        { name: "Tokyo, Japan", flag: "https://flagcdn.com/jp.svg", startTime: 2, endTime: 8, nextDayReached: false, cssClass: "japan", topPosition: 290 }
    ];

    const container = document.getElementById('canvas-container');

    // Function to dynamically create the session bars
    function createSessionBars() {
        tradingSessions.forEach(session => {
            if (session.nextDayReached) {
                createNextDaySessionBars(session);
            } else {
                createNormalSessionBar(session);
            }

            createFlagAndName(session);
        });
    }

    // Function to handle sessions that cross into the next day
    function createNextDaySessionBars(session) {
        const firstLeftPosition = (session.startTime / totalHours) * 100;
        const firstSessionWidth = ((24 - session.startTime) / totalHours) * 100;

        const secondLeftPosition = (0 / totalHours) * 100;
        const secondSessionWidth = (session.endTime / totalHours) * 100;

        createSessionDiv(firstLeftPosition, firstSessionWidth, session);
        createSessionDiv(secondLeftPosition, secondSessionWidth, session);
    }

    // Function to create normal session bars
    function createNormalSessionBar(session) {
        const leftPosition = (session.startTime / totalHours) * 100;
        const sessionWidth = ((session.endTime - session.startTime) / totalHours) * 100;

        createSessionDiv(leftPosition, sessionWidth, session);
    }

    // Helper to create session div (bar)
    function createSessionDiv(leftPosition, sessionWidth, session) {
        const sessionDiv = document.createElement('div');
        sessionDiv.classList.add('session-rect', session.cssClass);
        sessionDiv.style.left = `${leftPosition}%`;
        sessionDiv.style.width = `${sessionWidth}%`;
        sessionDiv.style.top = `${session.topPosition}px`;

        container.appendChild(sessionDiv);
    }

    // Create flag and name container
    function createFlagAndName(session) {
        const flagDiv = document.createElement('div');
        flagDiv.classList.add('flag-container', session.cssClass);
        flagDiv.style.top = `${session.topPosition}px`;
        const flagImg = document.createElement('img');
        flagImg.src = session.flag;
        const countryName = document.createElement('span');
        countryName.innerText = session.name;

        flagDiv.appendChild(flagImg);
        flagDiv.appendChild(countryName);
        container.appendChild(flagDiv);
    }

    // Function to dynamically update the needle position based on the current time
    function updateNeedlePosition() {
        const now = new Date();
        const currentHour = now.getHours();
        const currentMinute = now.getMinutes();
        const timeFraction = currentHour + currentMinute / 60;

        const needle = document.getElementById('needle');
        const currentTimeDiv = document.getElementById('current-time');

        const needlePosition = (timeFraction / totalHours) * 100;
        needle.style.left = `${needlePosition}%`;
        currentTimeDiv.style.left = `${needlePosition}%`;

        currentTimeDiv.innerHTML = `${now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}`;
    }

    // Create X-axis labels dynamically
    function createXAxisLabels() {
        const xAxis = document.getElementById('x-axis');
        for (let i = 1; i <= totalHours; i++) {
            const labelDiv = document.createElement('div');
            labelDiv.innerText = i;
            xAxis.appendChild(labelDiv);
        }
    }

    createSessionBars();
    createXAxisLabels();
    updateNeedlePosition();

    // Update needle every minute
    setInterval(updateNeedlePosition, 60000);
</script>

</body>
</html>
