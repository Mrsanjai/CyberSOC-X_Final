# app/windows_log_reader.py

import win32evtlog
import win32evtlogutil
import win32con
import datetime

def get_event_type_name(event_type):
    """Convert numeric event type to readable string"""
    event_types = {
        win32con.EVENTLOG_ERROR_TYPE: "Error",
        win32con.EVENTLOG_WARNING_TYPE: "Warning",
        win32con.EVENTLOG_INFORMATION_TYPE: "Information",
        win32con.EVENTLOG_AUDIT_SUCCESS: "Audit Success",
        win32con.EVENTLOG_AUDIT_FAILURE: "Audit Failure"
    }
    return event_types.get(event_type, f"Unknown ({event_type})")

def get_windows_logs(log_type="Security", max_logs=20):
    server = 'localhost'
    log = win32evtlog.OpenEventLog(server, log_type)
    
    flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
    logs = []

    try:
        events = win32evtlog.ReadEventLog(log, flags, 0)
        for i, event in enumerate(events):
            if i >= max_logs:
                break

            timestamp = event.TimeGenerated.Format() if event.TimeGenerated else str(datetime.datetime.now())
            message = event.StringInserts
            if isinstance(message, list):
                message = "\n".join([str(m) for m in message])
            else:
                message = str(message)

            log_entry = {
                "record_number": event.RecordNumber,
                "timestamp": timestamp,
                "event_type": get_event_type_name(event.EventType),
                "event_id": event.EventID,
                "category": event.EventCategory,
                "source": str(event.SourceName),
                "computer": str(event.ComputerName),
                "message": message
            }

            logs.append(log_entry)
    except Exception as e:
        logs.append({"error": f"Failed to read logs: {str(e)}"})
    finally:
        win32evtlog.CloseEventLog(log)

    return logs
