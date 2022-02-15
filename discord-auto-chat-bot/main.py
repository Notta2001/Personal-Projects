from selenium import webdriver;
from time import sleep;
from selenium.webdriver.chrome.service import Service;
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys;

# 1.  Declare browser variable
ser = Service("./chromedriver")
op = webdriver.ChromeOptions()
browser = webdriver.Chrome(service=ser, options=op)

# 2. Open a website
browser.get("https://discord.com/login");

sentences = ["Hi! I am Rebecca. And you?", "Nice to meet you.", "Where are you from?", "What do you do?", "What do you like to do in your free time?", "What is your phone number?", "Do you have Facebook?", "Thanks so much.", "I really appreciate…", "Excuse me.", "I am sorry.", "What do you think?"];

# 3. Fill in information and password
user = browser.find_element_by_name("email");
user.send_keys("fakegmail@gmail.com");

password = browser.find_element_by_name("password");
password.send_keys("fakepassword");

# 4. Login
user.send_keys(Keys.ENTER);
sleep(5);

# 5. Go to main page
browser.get("https://discord.com/channels/************/**********");
sleep(5);

# 6. Auto comment for 20 times
i = 0;
while i < 20:  
  browser.find_element_by_tag_name('body').send_keys(sentences[i%len(sentences)]);
  sleep(1);
  actions = ActionChains(browser);
  actions.send_keys(Keys.ENTER);
  actions.perform();
  i = i + 1;
  sleep(4);

# 7. Close page
sleep(10);
browser.close();