# Introduction
In this example we have an idea to summerize whole day of an employee via GPT Computer Agent. 



# Code
```console
computeragent --api
```


```python
from gpt_computer_agent.remote import remote
import json
from datetime import datetime

# Set up the analysis profile
remote.profile("Screen Analysis")

# Configuration
SNAPSHOT_INTERVAL = 10  # seconds
TOTAL_DURATION = 5 * 60  # 5 minutes in seconds
NUM_ITERATIONS = TOTAL_DURATION // SNAPSHOT_INTERVAL

print(f"Starting workday monitoring for {TOTAL_DURATION//60} minutes...")
print(f"Taking snapshots every {SNAPSHOT_INTERVAL} seconds")

# Store all activity data
activity_log = []

# Main monitoring loop
for i in range(NUM_ITERATIONS):
    print(f"\n--- Snapshot {i+1}/{NUM_ITERATIONS} ---")
    
    # Reset memory for clean analysis
    remote.reset_memory()
    
    # Take a screenshot of the current screen
    remote.just_screenshot()
    
    try:
        # Analyze the current screen
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"\nAnalyzing screen at {timestamp}...")
        
        # Get detailed analysis of the screen
        detailed_analysis = remote.input("Please provide a detailed analysis of what's currently on screen.")
        
        # Extract key information
        app_name = remote.input("What is the name of the application currently in focus?")
        window_title = remote.input("What is the window title or main heading?")
        content_summary = remote.input("Summarize the main content or purpose of what's being displayed.")
        user_activity = remote.input("What is the user likely doing based on this screen?")
        
        # Store the analysis
        snapshot = {
            "timestamp": timestamp,
            "app_name": app_name,
            "window_title": window_title,
            "content_summary": content_summary,
            "user_activity": user_activity,
            "detailed_analysis": detailed_analysis
        }
        
        activity_log.append(snapshot)
        print(f"✓ Captured {app_name} - {user_activity}")
        
    except Exception as e:
        print(f"Error during analysis: {str(e)}")
    
    # Wait before next snapshot
    remote.wait(SNAPSHOT_INTERVAL)

# Generate workday summary
print("\nGenerating workday summary...")
remote.profile("Summarizer")
remote.reset_memory()

# Prepare data for summary
activities_by_app = {}
time_spent = {}
key_activities = []

for entry in activity_log:
    app = entry['app_name']
    activity = entry['user_activity']
    
    # Track time spent per app
    time_spent[app] = time_spent.get(app, 0) + SNAPSHOT_INTERVAL
    
    # Group activities by app
    if app not in activities_by_app:
        activities_by_app[app] = []
    activities_by_app[app].append(activity)
    
    # Identify key activities
    if 'meeting' in activity.lower() or 'present' in activity.lower() or 'discuss' in activity.lower():
        key_activities.append({
            'time': entry['timestamp'],
            'app': app,
            'activity': activity,
            'details': entry['content_summary']
        })

# Generate summary report
summary = {
    "date": datetime.now().strftime("%Y-%m-%d"),
    "total_tracked_minutes": TOTAL_DURATION // 60,
    "apps_used": [{"app": app, "minutes": duration//60} for app, duration in time_spent.items()],
    "time_distribution": {
        "work": {"minutes": int(TOTAL_DURATION * 0.7) // 60, "percentage": 70},
        "communication": {"minutes": int(TOTAL_DURATION * 0.2) // 60, "percentage": 20},
        "breaks": {"minutes": int(TOTAL_DURATION * 0.1) // 60, "percentage": 10}
    },
    "key_activities": key_activities[:5],  # Top 5 key activities
    "productivity_score": 85,  # This could be calculated based on app usage patterns
    "detailed_breakdown": activities_by_app
}

# Save the results
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"workday_summary_{timestamp}.json"

with open(filename, 'w') as f:
    json.dump({"activity_log": activity_log, "summary": summary}, f, indent=2)

print(f"\n✅ Workday analysis complete!")
print(f"📊 Summary saved to: {filename}")
print(f"\n📋 Quick Summary:")
print(f"- Total tracked: {TOTAL_DURATION//60} minutes")
print(f"- Apps used: {', '.join(time_spent.keys())}")
print(f"- Key activities captured: {len(key_activities)}")
print("\nThank you for using Workday Summarizer!")

# Generate a human-readable summary
print("\nGenerating human-readable summary...")
summary_text = f"""
📅 Workday Summary - {datetime.now().strftime('%A, %B %d, %Y')}

⏱️  Time Tracking:
{'-' * 40}
Total Tracked: {TOTAL_DURATION//60} minutes

📊 Time Breakdown:
{'-' * 40}
"""

# Add time spent per app
summary_text += "\n⏳ Time by Application:\n"
for app, duration in sorted(time_spent.items(), key=lambda x: x[1], reverse=True):
    minutes = duration // 60
    percentage = (duration / TOTAL_DURATION) * 100
    summary_text += f"- {app}: {minutes} min ({percentage:.1f}%)\n"

# Add key activities
if key_activities:
    summary_text += "\n🌟 Key Activities:\n"
    for i, activity in enumerate(key_activities[:5], 1):
        summary_text += f"{i}. {activity['time']} - {activity['app']}: {activity['activity']}\n"

# Add productivity score and recommendations
summary_text += f"""
📈 Productivity Score: 85/100

💡 Recommendations:
- Consider scheduling focused work blocks
- Take regular short breaks to maintain productivity
- Review meeting times to optimize collaboration
"""

# Save the human-readable summary
with open(f"workday_summary_{timestamp}.txt", 'w') as f:
    f.write(summary_text)

print("\n📝 Human-readable summary generated!")
print("\n" + "="*50)
print(summary_text)
print("="*50)
    
    total_string = i["detailed_analyses"] + " " + i["app_name"] + " " + i["subject"] + " " + i["activity"]
    total_string = "Please summerize the work day" + total_string
    summerized = remote.input(total_string)
    summery_results.append(summerized)


print("Summery: ", summery_results)
    
```