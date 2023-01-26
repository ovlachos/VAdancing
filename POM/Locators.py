### Common PAGE
page_ID = {
    'scrollableRecyclerView': 'android:id/list',
}

page_XPATH = {
    'postsGrid': "//android.widget.Button[contains(@content-desc, 'Row 1, Column 1')]",
}

### LOG IN PAGE
loginPage_XPath = {
    'captchaTest': "//span[contains(@id,'meprmath_captcha')]",
    'userName': "//input[contains(@id,'user_login')]",
    'password': "//input[contains(@id,'user_pass')]",
    'captchaResponse': "//input[contains(@id,'meprmath_quiz')]",
    'LogIn_button': "//input[contains(@id,'wp-submit')]",

}

### HOME PAGE
homePage_XPath = {
    'courses': "//a[contains(@href,'https://thebluesroom.com/course-library/')]",

}

### Course Library
TopicLib_XPath = {
    # 'Beginners Survival Kit': "//a[contains(text(),'Beginners Survival Kit')]",
    'Essential Skills': "//a[contains(text(),'Essential Skills')]",
    'Musicality': "//a[contains(text(),'Musicality')]",
    'Solo Skills': "//a[contains(text(),'Solo Skills')]",
    'Vocabulary': "//a[contains(text(),'Vocabulary')]",
    'Idiom Dances': "//a[contains(text(),'Idiom Dances')]",
    'Top Tips and Q&As': "//a[contains(text(),'Top Tips and Q&As')]",
    'Practice With Us': "//a[contains(text(),'Practice With Us')]",
    'Choreographies': "//a[contains(text(),'Choreographies')]",
    'Challenges': "//a[contains(text(),'Challenges')]",

}

### CourseCategories
courseCategory_XPath = {
    # 'startCourseButtons': "//div[contains(@style,'block')]//a",
    'startCourseButtons': "//div[(contains(@style,'block'))]//a[contains(@class,'et_pb_button')]",
    # 'Beginners Survival Kit': "//a[contains(text(),'Beginners Survival Kit')]",
}

### Course Videos
courseVideos_XPath = {
    'videoThumbs': "//figure[contains(@class,'thumb')]//img[contains(@class,'thumb')]",
    'swiperNext': "//div[contains(@class,'swiper-button-next')]",
    'swiperPrev': "//div[contains(@class,'swiper-button-prev')]",
}
