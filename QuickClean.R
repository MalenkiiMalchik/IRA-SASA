require(tidyverse)
require(rvest)

# Grabbing the table of propaganda accounts
raw = read_html("https://www.reddit.com/wiki/suspiciousaccounts")
table = raw %>% 
  html_nodes(.,xpath="/html/body/div[1]/div/div/div/div[2]/div/div/div/div[2]/div[3]/div[1]/div[3]/div/div[1]/div/table") %>% 
  html_table()
table = data.frame(table)

# Cleaning it to remove "u/"
table = table %>% mutate(Username = str_remove(Username, "u/")) %>% rename(author = Username)

# Writing a CSV for python
write_csv(table, "table-of-usernames.csv")

# Reading in set of exposed authors
final_cal <- read_csv("authorset.csv")

# Cleaning out duplicates and any propaganda accounts
final_cal2 = final_cal %>% 
  rename("Author" = "0_1") %>% 
  mutate(AuthDup = as.numeric(duplicated(Author))) %>% 
  filter(AuthDup==0) %>%
  anti_join(table)

# First pass at cleaning out non-people
final_cal2 = final_cal2 %>% 
  filter((Author == "[deleted]")==FALSE) %>% 
  filter((Author == "[removed]")==FALSE) %>% 
  filter((Author == "Automoderator")==FALSE) %>% 
  filter((Author == "AutoModerator")==FALSE) %>% 
  filter((Author == "transcribot")==FALSE) %>% 
  filter((Author == "USPSbot")==FALSE) %>% 
  filter((Author == "feetpicsbot")==FALSE)

write_csv(final_cal2, "Comment-Author-List-Clean.csv")

############################ Random Authors - Same cleanings Steps ##################################

rand_cal <- read_csv("rand_authorset.csv")

rand_cal2 = rand_cal %>% 
  rename("Author" = "0_1") %>% 
  mutate(AuthDup = as.numeric(duplicated(Author))) %>% 
  filter(AuthDup==0) %>%
  anti_join(table)

rand_cal2 = rand_cal2 %>% 
  filter((Author == "[deleted]")==FALSE) %>% 
  filter((Author == "[removed]")==FALSE) %>% 
  filter((Author == "Automoderator")==FALSE) %>% 
  filter((Author == "AutoModerator")==FALSE) %>% 
  filter((Author == "transcribot")==FALSE) %>% 
  filter((Author == "USPSbot")==FALSE) %>% 
  filter((Author == "feetpicsbot")==FALSE)

write_csv(rand_cal2, "Comment-Author-List-Clean-rand.csv")
