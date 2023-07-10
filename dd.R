pacman::p_load(rio,dplyr)

data <- import("../../../mobidep/total_migrations.csv")

data %>% 
  filter(DRACT == '13') %>% 
  select(DRAN,IPONDI) %>% 
  mutate(IPONDI = as.numeric(IPONDI)) %>% 
  write.csv("../../../mobidep/test1.csv",row.names = F)
