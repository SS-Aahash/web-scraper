from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

start = time.perf_counter()
print("\nYou can fetch upto 10 records")
records_needed = int(input("N.o of records needed(default:6): ") or 6)
if(records_needed>10):
     print("You can only fetch upto 10 records")
     exit()

print('\nScraper_booting...')

def get_elemeent_text(xpath):
    try:
        return driver.find_element(By.XPATH, xpath).text
    except:
        return 'N/A'

data = []

options = Options()
options.add_argument("--headless") #comment this to see the scrapper work live in browser

driver = webdriver.Chrome(options=options)  
try:
    print("\nOpening website...")
    driver.get("https://rera.odisha.gov.in/projects/project-list")
except:
    print("Site is unrechable")

print('\nPlease wait...')
for i in range(records_needed):
    WebDriverWait(driver,10).until( 
        EC.presence_of_all_elements_located((By.CSS_SELECTOR,".card-body.d-md-flex"))
    )
    
    projects = driver.find_elements(By.CSS_SELECTOR,".card-body.d-md-flex")
    project = projects[i]


    view_btn = project.find_element(By.XPATH,".//a[contains(text(),'View Details')]")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", view_btn)
    time.sleep(1)  
    view_btn.click()

    time.sleep(2)

    project_name = get_elemeent_text("//label[contains(text(), 'Project Name')]/following-sibling::strong")
    rera_number = get_elemeent_text("//label[contains(text(), 'RERA Regd. No.')]/following-sibling::strong")

    promoter_tab = driver.find_element(By.XPATH, "//a[contains(text(),'Promoter Details')]")
    time.sleep(1)
    promoter_tab.click()

    time.sleep(1)

                                    
    promoter_name = get_elemeent_text("//label[contains(text(),'Company Name') or contains(text(),'Propietory Name')]/following-sibling::strong")
    address = get_elemeent_text("//label[contains(text(),'Registered Office Address') or contains(text(),'Current Residence Address')]/following-sibling::strong")
    gst_number = get_elemeent_text("//label[contains(text(),'GST No.')]/following-sibling::strong")
    
    data.append({
        "Project Name" : project_name,
        "Promoter/Company Name" : promoter_name,
        "Registered Office Address" : address,
        "RERA Regd. No." : rera_number,
        "GST No." : gst_number
    })

    driver.back() 
    print(f"\nRecords Fetched: {i+1}")
driver.quit()

print("Browser operations successfull\n")

for items in data:
        for key,value in items.items():
             print(f'{key}: {value}') 
        print("\n")

end = time.perf_counter()
elapsed = end - start

if elapsed < 60:
    print(f"Fetched {records_needed} records({elapsed:.2f} seconds)")
else:
    minutes = int(elapsed // 60)
    seconds = elapsed % 60
    print(f"Fetched {records_needed} records({minutes} minute & {seconds:.2f} seconds)")