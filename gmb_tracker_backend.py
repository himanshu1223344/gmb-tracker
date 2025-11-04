# ✅ ULTIMATE INTERACTIVE GMB RANKING TRACKER v2.0
# 🎯 With Menu System + Multi-Location + Pagination Support
# 🚀 OPTIMIZED - CRAWL ALL PAGES + EARLY SKIP + BALANCED SPEED
# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import random
import pandas as pd
from datetime import datetime
import json
import os
from fake_useragent import UserAgent
import warnings
import logging
import atexit
import gc

warnings.filterwarnings("ignore")
logging.getLogger("undetected_chromedriver").setLevel(logging.CRITICAL)

def cleanup_on_exit():
    gc.collect()

atexit.register(cleanup_on_exit)

# ============================================================================
# 🎯 INTERACTIVE MENU SYSTEM
# ============================================================================

def display_menu():
    """Display interactive selection menu"""
    if os.environ.get('CUSTOM_BUSINESS') or os.environ.get('CUSTOM_KEYWORDS'):
        return
    
    print(f"\n\n{'='*80}")
    print("🎯 ULTIMATE GMB RANKING TRACKER - BUSINESS SELECTOR")
    print(f"{'='*80}\n")
    
    print("📍 SELECT YOUR OPTION:\n")
    
    print("1️⃣  Dr. Prashansa - MALAD, MUMBAI")
    print("    Business: Dr. Prashansa Raut Dalvi")
    print("    Location: Malad, Mumbai")
    print("    Keywords: 18 Gynecology Keywords")
    print()
    
    print("2️⃣  Dr. Prashansa - ANDHERI, MUMBAI")
    print("    Business: Dr. Prashansa Raut-Dalvi")
    print("    Location: Andheri, Mumbai")
    print("    Keywords: 18 Gynecology Keywords")
    print()
    
    print("3️⃣  Dr. Prashansa - PALGHAR")
    print("    Business: Dr Prashansa Raut-Dalvi")
    print("    Location: Palghar")
    print("    Keywords: 18 Gynecology Keywords")
    print()
    
    print("4️⃣  ALL 3 LOCATIONS (54 Keywords Total)")
    print("    Tracks: Malad + Andheri + Palghar")
    print("    Keywords: 18 × 3 = 54 Total")
    print()
    
    print("5️⃣  CUSTOM TRACKING")
    print("    Enter your own business name, location, and keywords")
    print()
    
    print(f"{'='*80}\n")

def get_user_selection():
    """Get user input and validate"""
    while True:
        try:
            choice = input("📌 Enter your choice (1-5): ").strip()
            if choice in ['1', '2', '3', '4', '5']:
                return choice
            else:
                print("❌ Invalid choice! Please enter 1, 2, 3, 4, or 5")
        except KeyboardInterrupt:
            print("\n\n⚠️ Tracking cancelled by user")
            exit()
        except Exception as e:
            print(f"❌ Error: {e}")

def get_configuration(choice):
    """Get configuration based on user selection"""
    
    if choice == '1':
        return {
            'mode': 'single',
            'location_name': 'Malad',
            'business_name': 'Dr. Prashansa Raut Dalvi',
            'location': 'Malad, Mumbai',
            'business_names': [
                'Dr. Prashansa Raut Dalvi',
                'Dr Prashansa Raut',
                'Prashansa Raut Dalvi'
            ]
        }
    
    elif choice == '2':
        return {
            'mode': 'single',
            'location_name': 'Andheri',
            'business_name': 'Dr. Prashansa Raut-Dalvi',
            'location': 'Andheri, Mumbai',
            'business_names': [
                'Dr. Prashansa Raut-Dalvi',
                'Dr Prashansa Raut Andheri',
                'Prashansa Raut-Dalvi'
            ]
        }
    
    elif choice == '3':
        return {
            'mode': 'single',
            'location_name': 'Palghar',
            'business_name': 'Dr Prashansa Raut-Dalvi',
            'location': 'Palghar',
            'business_names': [
                'Dr Prashansa Raut-Dalvi',
                'Dr Prashansa Raut',
                'Dr. Prashansa Raut',
                'Prashansa Raut',
                'Dr. Prashansa Raut Palghar',
                'Prashansa Raut Gynaecologist'
            ]
        }
    
    elif choice == '4':
        return {
            'mode': 'multi',
            'locations': [
                {
                    'location_name': 'Malad',
                    'business_name': 'Dr. Prashansa Raut Dalvi',
                    'location': 'Malad, Mumbai',
                    'business_names': [
                        'Dr. Prashansa Raut Dalvi',
                        'Dr Prashansa Raut',
                        'Prashansa Raut Dalvi'
                    ]
                },
                {
                    'location_name': 'Andheri',
                    'business_name': 'Dr. Prashansa Raut-Dalvi',
                    'location': 'Andheri, Mumbai',
                    'business_names': [
                        'Dr. Prashansa Raut-Dalvi',
                        'Dr Prashansa Raut Andheri',
                        'Prashansa Raut-Dalvi'
                    ]
                },
                {
                    'location_name': 'Palghar',
                    'business_name': 'Dr Prashansa Raut-Dalvi',
                    'location': 'Palghar',
                    'business_names': [
                        'Dr Prashansa Raut-Dalvi',
                        'Dr. Prashansa Raut Palghar',
                        'Prashansa Raut Gynaecologist'
                    ]
                }
            ]
        }
    
    elif choice == '5':
        business_name = os.environ.get('CUSTOM_BUSINESS')
        location = os.environ.get('CUSTOM_LOCATION')
        keywords_str = os.environ.get('CUSTOM_KEYWORDS')
        
        if not all([business_name, location, keywords_str]):
            print("\n🎯 CUSTOM SETUP\n")
            business_name = input("Enter business name: ").strip()
            location = input("Enter location (e.g., Malad, Mumbai): ").strip()
            
            print("\nEnter keywords (one per line, press Enter twice when done):")
            keywords = []
            while True:
                kw = input(f"Keyword {len(keywords) + 1}: ").strip()
                if not kw:
                    if keywords:
                        break
                    else:
                        print("❌ Please enter at least one keyword")
                        continue
                keywords.append(kw)
        else:
            keywords = [kw.strip() for kw in keywords_str.split('\n') if kw.strip()]
        
        return {
            'mode': 'custom',
            'location_name': 'Custom',
            'business_name': business_name,
            'location': location,
            'business_names': [business_name],
            'keywords': keywords
        }

# ============================================================================
# 🔥 MAIN TRACKER CLASS
# ============================================================================

class AdvancedGMBRankingTracker:
    """🔥 ULTIMATE GMB Ranking Tracker - OPTIMIZED FOR CRAWLING ALL PAGES"""
    
    def __init__(self, headless=False, use_google_search=True):
        self.headless = headless
        self.use_google_search = use_google_search
        self.ua = UserAgent()
        self.driver = None
        self.all_businesses = []
    
    def get_random_user_agent(self):
        return self.ua.random
    
    def setup_driver(self):
        """Advanced Driver Configuration with Anti-Detection"""
        options = uc.ChromeOptions()
        
        if self.headless:
            options.add_argument('--headless=new')
        
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--disable-features=IsolateOrigins,site-per-process')
        options.add_argument('--disable-web-security')
        options.add_argument('--allow-running-insecure-content')
        options.add_argument('--disable-infobars')
        options.add_argument('--disable-extensions')
        options.add_argument('--profile-directory=Default')
        options.add_argument('--disable-gpu')
        
        screen_resolutions = [
            '--window-size=1920,1080',
            '--window-size=1366,768',
            '--window-size=1536,864',
        ]
        options.add_argument(random.choice(screen_resolutions))
        options.add_argument(f'user-agent={self.get_random_user_agent()}')
        
        prefs = {
            "profile.default_content_setting_values.notifications": 2,
            "profile.default_content_setting_values.geolocation": 2,
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
            "webrtc.ip_handling_policy": "disable_non_proxied_udp"
        }
        options.add_experimental_option("prefs", prefs)
        
        try:
            self.driver = uc.Chrome(options=options, version_main=None)
        except Exception as e:
            print(f"⚠️ Driver setup retry: {e}")
            time.sleep(2)
            self.driver = uc.Chrome(options=options, version_main=None)
        
        try:
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            self.driver.execute_script("Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]})")
        except:
            pass
        
        return self.driver
    
    def human_like_delay(self, min_delay=1.5, max_delay=3):
        """OPTIMIZED: Balanced delays - not too fast, not too slow"""
        delay = random.uniform(min_delay, max_delay)
        time.sleep(delay)
    
    def move_mouse_randomly(self):
        """Random mouse movements - OPTIMIZED"""
        try:
            actions = ActionChains(self.driver)
            for _ in range(random.randint(1, 3)):
                x_offset = random.randint(-50, 50)
                y_offset = random.randint(-50, 50)
                actions.move_by_offset(x_offset, y_offset).perform()
                time.sleep(random.uniform(0.05, 0.1))
        except:
            pass
    
    def scroll_smoothly(self, scrolls=3):
        """Smooth scrolling simulation - OPTIMIZED"""
        for i in range(scrolls):
            scroll_amount = random.randint(200, 400)
            try:
                self.driver.execute_script(f'window.scrollBy(0, {scroll_amount})')
            except:
                pass
            time.sleep(random.uniform(0.2, 0.4))
    
    def check_gmb_ranking(self, keyword, location, business_name, business_names, max_results=100):
        """Main ranking check function"""
        self.all_businesses = []
        
        print(f"\n{'='*80}")
        print(f"🎯 TRACKING: {keyword}")
        print(f"   📍 Location: {location}")
        print(f"   🏢 Business: {business_name}")
        print(f"{'='*80}")
        
        try:
            if not self.driver:
                self.setup_driver()
            
            search_query = f"{keyword} in {location}"
            url = f"https://www.google.com/search?q={search_query.replace(' ', '+')}&tbm=lcl"
            
            print(f"🌐 URL: {url}")
            
            self.driver.get(url)
            self.human_like_delay(3, 5)
            self.move_mouse_randomly()
            
            return self._track_multi_page_google_search(keyword, location, business_name, business_names, max_results)
        
        except Exception as e:
            print(f"\n❌ ERROR: {str(e)}")
            return self._create_error_result(keyword, location, business_name, str(e))
    
    def _track_multi_page_google_search(self, keyword, location, business_name, business_names, max_results):
        """🔥 CRAWL ALL PAGES - SKIP ON FOUND"""
        position = 0
        checked_names = set()
        page_number = 1
        max_pages = 999  # CRAWL ALL PAGES
        all_businesses_found = []
        found_flag = False
        
        while page_number <= max_pages and position < max_results:
            print(f"\n📄 === PAGE {page_number} ===")
            
            time.sleep(1.5)  # OPTIMIZED: Faster page load
            self.scroll_smoothly(2)
            time.sleep(1)
            
            business_selectors = [
                'div.VkpGBb',
                'div[jscontroller][data-hveid]',
                'div.rllt__details',
                'div[data-cid]',
            ]
            
            businesses = []
            for selector in business_selectors:
                try:
                    businesses = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if businesses:
                        print(f"   ✅ Found {len(businesses)} results on page {page_number}")
                        break
                except:
                    continue
            
            if not businesses:
                print(f"   ⚠️ No businesses found on page {page_number}")
                break
            
            new_results_found = False
            for business in businesses:
                try:
                    name = self._extract_business_name_search(business)
                    
                    if not name or name in checked_names:
                        continue
                    
                    checked_names.add(name)
                    position += 1
                    new_results_found = True
                    
                    self.all_businesses.append({
                        'position': position,
                        'name': name,
                        'page': page_number
                    })
                    
                    all_businesses_found.append({
                        'position': position,
                        'name': name,
                        'page': page_number
                    })
                    
                    # Display business
                    print(f"\n  {'─'*76}")
                    print(f"  🏢 POSITION #{position:2d} (Page {page_number})")
                    print(f"  {'─'*76}")
                    print(f"  📍 {name}")
                    print(f"  {'─'*76}")
                    
                    # Check for match
                    for business_name_check in business_names:
                        if self._is_business_match(business_name_check, name):
                            print(f"\n{'🎉'*38}")
                            print(f"✅ ✅ ✅ FOUND YOUR BUSINESS! ✅ ✅ ✅")
                            print(f"{'🎉'*38}\n")
                            print(f"📍 Position: #{position}")
                            print(f"📄 Page: {page_number}")
                            print(f"🎯 Matched: {name}")
                            print(f"🏢 Your Business: {business_name}")
                            print(f"\n{'🎉'*38}\n")
                            
                            found_flag = True
                            break
                    
                    if found_flag:
                        break
                    
                    if position >= max_results:
                        break
                
                except:
                    continue
            
            if found_flag:
                # OPTIMIZED: Skip remaining pages on found
                print(f"\n✅ Business found! Skipping remaining pages...")
                break
            
            if not new_results_found:
                print(f"   ⚠️ No new unique results on page {page_number}")
                break
            
            if position >= max_results:
                break
            
            # Try to click next page
            next_button_found = self._click_next_page()
            
            if not next_button_found:
                print(f"\n   ⚠️ No 'Next' button found. Reached last page.")
                break
            
            page_number += 1
            self.human_like_delay(1, 2)  # OPTIMIZED: Faster page transition
        
        if found_flag:
            return {
                'keyword': keyword,
                'location': location,
                'searched_business': business_name,
                'found_business_name': name,
                'position': position,
                'page': page_number,
                'found': True,
                'total_checked': position,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
        
        # ENHANCED: Show summary
        print(f"\n\n{'='*80}")
        print(f"📊 ALL {position} BUSINESSES CHECKED")
        print(f"{'='*80}\n")
        
        for biz in all_businesses_found:
            print(f"  #{biz['position']:2d} (Page {biz['page']}): {biz['name']}")
        
        print(f"\n{'='*80}\n")
        print(f"❌ NOT FOUND in {position} results across {page_number} pages")
        print(f"   🔍 Searched for: {business_name}")
        print(f"\n{'='*80}\n")
        
        return self._create_not_found_result(keyword, location, business_name, position)
    
    def _click_next_page(self):
        """Click the 'Next' button to navigate to next page"""
        next_button_selectors = [
            'a#pnnext',
            'a[aria-label="Next page"]',
            'a[aria-label="Next"]',
        ]
        
        for selector in next_button_selectors:
            try:
                next_button = self.driver.find_element(By.CSS_SELECTOR, selector)
                
                if next_button and next_button.is_displayed():
                    print(f"   🔄 Clicking 'Next' button...")
                    
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", next_button)
                    time.sleep(0.5)
                    
                    try:
                        next_button.click()
                    except:
                        self.driver.execute_script("arguments[0].click();", next_button)
                    
                    return True
            except:
                continue
        
        return False
    
    def _extract_business_name_search(self, business_element):
        """Extract business name from Google Search"""
        name_selectors = [
            'div[role="heading"]',
            'span.OSrXXb',
            'div.dbg0pd',
            'a span',
        ]
        
        for selector in name_selectors:
            try:
                element = business_element.find_element(By.CSS_SELECTOR, selector)
                name = element.text.strip() or element.get_attribute('aria-label')
                if name and len(name) > 3:
                    name = name.split(' -')[0].split('(')[0].strip()
                    name = ' '.join(name.split())
                    if len(name) > 3:
                        return name
            except:
                continue
        
        try:
            text = business_element.text.strip()
            if text:
                lines = text.split('\n')
                for line in lines[:3]:
                    line = line.split(' -')[0].split('(')[0].strip()
                    line = ' '.join(line.split())
                    if len(line) > 3 and len(line) < 100:
                        return line
        except:
            pass
        
        return None
    
    def _is_business_match(self, target_name, found_name):
        """Fuzzy matching - ULTRA AGGRESSIVE"""
        target = ' '.join(target_name.lower().split())
        found = ' '.join(found_name.lower().split())
        
        # Remove common words
        for word in ['dr', 'doctor', 'clinic', 'hospital', 'center', 'the', 'in', 'at', 'and', 'or', 'gynaecologist', 'gynecologist', '-', '.']:
            target = target.replace(word, ' ').replace('  ', ' ')
            found = found.replace(word, ' ').replace('  ', ' ')
        
        target = target.strip()
        found = found.strip()
        
        # Exact match
        if target == found:
            return True
        
        if target in found or found in target:
            return True
        
        # Word overlap
        target_words = set(target.split())
        found_words = set(found.split())
        
        if target_words and (target_words == found_words or target_words.issubset(found_words)):
            return True
        
        common = target_words & found_words
        if len(target_words) > 0 and len(common) / len(target_words) >= 0.3:
            return True
        
        return False
    
    def _clean_business_name(self, name):
        """Clean business name for matching"""
        import re
        name = name.lower()
        name = re.sub(r'[^\w\s]', '', name)
        stopwords = ['dr', 'doctor', 'clinic', 'hospital', 'center', 'the', 'in', 'at', 'and', 'or']
        words = [w for w in name.split() if w not in stopwords]
        return ' '.join(words)
    
    def _create_error_result(self, keyword, location, business_name, error):
        return {
            'keyword': keyword,
            'location': location,
            'searched_business': business_name,
            'found_business_name': None,
            'position': None,
            'page': None,
            'found': False,
            'error': error,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def _create_not_found_result(self, keyword, location, business_name, checked):
        return {
            'keyword': keyword,
            'location': location,
            'searched_business': business_name,
            'found_business_name': None,
            'position': None,
            'page': None,
            'found': False,
            'total_checked': checked,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def close(self):
        """✅ Complete resource cleanup"""
        if self.driver:
            try:
                self.driver.quit()
            except OSError as e:
                if "handle is invalid" not in str(e).lower():
                    try:
                        self.driver.close()
                    except:
                        pass
            except Exception:
                try:
                    self.driver.close()
                except:
                    pass
            finally:
                self.driver = None
                gc.collect()

# ============================================================================
# 🚀 MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    
    display_menu()
    choice = get_user_selection()
    config = get_configuration(choice)
    
    DEFAULT_KEYWORDS = [
        "PCOD Treatment",
        "Female Gynaecologist",
        "IVF Treatment",
        "Best Gynaecologist",
        "Infertility Treatment",
        "High-Risk Pregnancy",
        "Endometriosis specialist",
        "Hormone Replacement Therapy",
        "Endometriosis Treatment",
        "Obstetrician-gynecologist",
        "Ovarian Cyst Treatment",
        "PCOS Treatment",
        "Menopause Treatment",
        "Menstrual Disorders Treatment",
        "Gynecological Infection Treatment",
        "Menorrhagia Treatment",
        "Women's Health Clinic",
        "Uterine Prolapse Treatment"
    ]
    
    tracker = AdvancedGMBRankingTracker(headless=False, use_google_search=True)
    all_results = []
    
    try:
        if config['mode'] == 'single':
            keywords = DEFAULT_KEYWORDS
            location_name = config['location_name']
            business_name = config['business_name']
            location = config['location']
            business_names = config['business_names']
            
            print(f"\n\n{'#'*80}")
            print(f"📍 TRACKING: {location_name.upper()}")
            print(f"{'#'*80}\n")
            
            for idx, keyword in enumerate(keywords, 1):
                print(f"\n\n{'#'*60}")
                print(f"📌 KEYWORD {idx}/{len(keywords)}")
                print(f"{'#'*60}")
                
                result = tracker.check_gmb_ranking(keyword, location, business_name, business_names, max_results=100)
                all_results.append(result)
                
                pd.DataFrame(all_results).to_csv('gmb_ranking_progress.csv', index=False)
                
                if idx < len(keywords):
                    wait_time = random.randint(6, 10)  # OPTIMIZED: Faster wait
                    print(f"\n⏳ Waiting {wait_time}s before next keyword...")
                    time.sleep(wait_time)
        
        elif config['mode'] == 'multi':
            total_keywords = len(DEFAULT_KEYWORDS) * len(config['locations'])
            current = 0
            
            for location_config in config['locations']:
                print(f"\n\n{'#'*80}")
                print(f"📍 TRACKING LOCATION: {location_config['location_name'].upper()}")
                print(f"{'#'*80}\n")
                
                for idx, keyword in enumerate(DEFAULT_KEYWORDS, 1):
                    current += 1
                    print(f"\n{'#'*60}")
                    print(f"📌 [{current}/{total_keywords}] {location_config['location_name']} - {idx}/{len(DEFAULT_KEYWORDS)}")
                    print(f"{'#'*60}")
                    
                    result = tracker.check_gmb_ranking(
                        keyword,
                        location_config['location'],
                        location_config['business_name'],
                        location_config['business_names'],
                        max_results=100
                    )
                    
                    result['location_name'] = location_config['location_name']
                    all_results.append(result)
                    
                    pd.DataFrame(all_results).to_csv('gmb_ranking_progress.csv', index=False)
                    
                    if current < total_keywords:
                        wait_time = random.randint(4, 8)  # OPTIMIZED: Faster wait
                        print(f"\n⏳ Waiting {wait_time}s...")
                        time.sleep(wait_time)
        
        elif config['mode'] == 'custom':
            keywords = config.get('keywords', DEFAULT_KEYWORDS)
            location_name = 'Custom'
            business_name = config['business_name']
            location = config['location']
            business_names = config['business_names']
            
            print(f"\n\n{'#'*80}")
            print(f"📍 CUSTOM TRACKING")
            print(f"{'#'*80}\n")
            
            for idx, keyword in enumerate(keywords, 1):
                print(f"\n{'#'*60}")
                print(f"📌 KEYWORD {idx}/{len(keywords)}")
                print(f"{'#'*60}")
                
                result = tracker.check_gmb_ranking(keyword, location, business_name, business_names, max_results=100)
                all_results.append(result)
                
                pd.DataFrame(all_results).to_csv('gmb_ranking_progress.csv', index=False)
                
                if idx < len(keywords):
                    wait_time = random.randint(4, 8)  # OPTIMIZED: Faster wait
                    print(f"\n⏳ Waiting {wait_time}s before next keyword...")
                    time.sleep(wait_time)
    
    finally:
        tracker.close()
    
    df = pd.DataFrame(all_results)
    filename = f'gmb_ranking_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    df.to_csv(filename, index=False)
    
    print(f"\n\n{'='*80}")
    print("📊 FINAL RANKING REPORT")
    print(f"{'='*80}\n")
    
    found_df = df[df['found'] == True]
    if len(found_df) > 0:
        print("✅✅✅ FOUND RANKINGS ✅✅✅\n")
        for _, row in found_df.iterrows():
            print(f"  🎯 KEYWORD: {row['keyword']}")
            print(f"     Position: #{int(row['position'])}")
            print(f"     Page: {int(row['page'])}")
            print(f"     Business: {row['found_business_name']}")
            print()
    
    not_found = df[df['found'] == False]
    if len(not_found) > 0:
        print(f"\n❌ NOT FOUND ({len(not_found)} keywords)\n")
        for _, row in not_found.iterrows():
            checked = row.get('total_checked', 0)
            print(f"  ❌ {row['keyword']}")
            print(f"     Checked: {checked} businesses")
            print()
    
    total_keywords = len(df)
    total_found = len(found_df)
    success_rate = (total_found / total_keywords * 100) if total_keywords > 0 else 0
    
    print(f"\n{'='*80}")
    print("📈 STATISTICS")
    print(f"{'='*80}")
    print(f"Total Keywords Tracked: {total_keywords}")
    print(f"✅ Keywords Found: {total_found}")
    print(f"❌ Keywords Not Found: {total_keywords - total_found}")
    print(f"📊 Success Rate: {success_rate:.1f}%")
    print(f"\n💾 Full Report saved: {filename}")
    print(f"{'='*80}\n")
