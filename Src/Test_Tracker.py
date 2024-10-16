import asyncio
import Torrent as TorrentClass
import Tracker as TrackerClass 
import tkinter as tk
from tkinter import filedialog

async def main():
    root = tk.Tk()
    root.withdraw()

    filePath = filedialog.askopenfilename()
    # Create a mock Torrent object for testing
    Torrent = TorrentClass.Torrent(filePath)    
    # Create the Tracker instance
    tracker = TrackerClass.Tracker(Torrent) 
    
    # Test the Connect method
    try:
        tracker_response = await tracker.Connect(first=True, uploaded=0, downloaded=0)
        print(tracker_response)
    except ConnectionError as e:
        print(f"Failed to connect to tracker: {e}")
    finally:
        await tracker.close()

# Run the async test function
if __name__ == "__main__":
    asyncio.run(main())