# Test List

- Loading settings
  - Loading file
    - [ ] Load nonexistant file
    - [ ] Load non-Yaml file
  - Checking settings 
    - [ ] Twitch credentials do not exist
    - [ ] Twitch credentials do not have client_id
    - [ ] Twitch credentials do not have secret
    - [ ] Twitter credentials do not have consumer key
    - [ ] Twitter credentials do not have consumer_secret
    - [ ] Twitter credentials do not have bearer_token
    - [ ] Twitter credentials do not have access_key
    - [ ] Twitter credentials do not have access_secret
    - [ ] Polling settings is a number
    - [ ] Verify all streamers have a twitch_user
    - [ ] Verify the provided settings for each user are correct
  - Function validation
    - [X] Verify posted twitter messages