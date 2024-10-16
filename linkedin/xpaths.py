class XPath:
    SEARCH_BOX = '//*[@id="global-nav-typeahead"]/input'
    JOBS_BUTTON = '//*[@id="search-reusables__filters-bar"]/ul/li[1]/button'
    POSTS_BUTTON = '//*[@id="navigational-filter_resultType"]'
    DROPDOWN_JOBS_OPTION = '//*[@id="ember6335"]'
    DATE_POSTED_BUTTON = '//*[@id="searchFilter_timePostedRange"]'
    _DATE_OPTION_PATTERN = '//*[contains(@id, "artdeco-hoverable-artdeco-gen")]'
    ANY_TIME_OPTION = _DATE_OPTION_PATTERN + '/div[1]/div/form/fieldset/div[1]/ul/li[1]/label'
    PAST_MONTH_OPTION = _DATE_OPTION_PATTERN + '/div[1]/div/form/fieldset/div[1]/ul/li[2]/label'
    PAST_WEEK_OPTION = _DATE_OPTION_PATTERN + '/div[1]/div/form/fieldset/div[1]/ul/li[3]/label'
    PAST_DAY_OPTION = _DATE_OPTION_PATTERN + '/div[1]/div/form/fieldset/div[1]/ul/li[4]/label'
    SHOW_RESULTS_BUTTON_TEXT = 'Apply current filter to show'
    SHOW_RESULTS_BUTTON = f'//button[contains(@aria-label, "{SHOW_RESULTS_BUTTON_TEXT}")]'
    NUM_RESULTS = '//*[@id="main"]/div/div[2]/div[1]/header/div[1]/small/div/span'


xpaths = XPath()
