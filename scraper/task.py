import schedule
import time
import fetchSourceforgeProducts

def run_script():
    # Code to run your script
    # For example:
    fetch_sourceforge_products.main()

schedule.every().minute.do(run_script)

while True:
    schedule.run_pending()
    time.sleep(1)