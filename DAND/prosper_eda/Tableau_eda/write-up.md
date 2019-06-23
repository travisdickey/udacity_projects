# Create a Tableau Story

[Explore Prosper Loan Data -- before Feedback](https://public.tableau.com/profile/travis.dickey#!/vizhome/Udacity--CreateTableauStoryProject/ExploringProsperLoanData)

[Explore Prosper Loan Data -- after Feedback](https://public.tableau.com/profile/travis.dickey#!/vizhome/Udacity--CreateTableauStoryProject--afterFeedback/ExploringProsperLoanData)

[Loan Data from Prosper](https://www.google.com/url?q=https://s3.amazonaws.com/udacity-hosted-downloads/ud651/prosperLoanData.csv&sa=D&ust=1511184905769000&usg=AFQjCNHfzkzdWPUSMFMdz5RXTbNK3jcWdQ)

[Data Dictionary](https://docs.google.com/spreadsheets/d/1gDyi_L4UvIrLTEC6Wri5nbaMmkGmLQBk-Yx3z0XDEtI/edit#gid=0)

## Summary
I examined the Prosper loan dataset, beginning with an exploration of borrower demographics then moving to a close look at Prosper's assessment of credit risk. Risk assessment requires a rather complex analysis of a range of variables. Simply relying on credit score, income, or debt-to-income-ratio will not make for solid predictions. It is unclear from the data exactly what variables Prosper uses in its formula for risk assessment, but it is clear that they made an adjustment to their formula after 2008, which seems to have improved their credit risk assessment.

## Design
One of the first design choices I had to make was whether to use captions or buttons in my story. I chose captions because I felt the charts would need a bit of explanation, and I felt they would help me give context to the overall story.

I chose to begin my story with basic exploration of demographics. I wanted the viewer to understand the scope of the dataset and in particular the breakdown by state and how the number of loans have changed over time. Clearly a map was the best choice to display the breakdown by state, and a line chart is generally the best design choice for change over time. I also wanted the viewer to get a sense of the range of borrower income, credit score, employment status, etc. I used bar charts and histograms to convey this information and set them in dashboards so that viewers could explore the data by filtering through the various categories.

Following the exploration of basics, I began to delve deeper into the area of primary focus, Prosper's credit risk assessment. From the [data dictionary](https://docs.google.com/spreadsheets/d/1gDyi_L4UvIrLTEC6Wri5nbaMmkGmLQBk-Yx3z0XDEtI/edit#gid=0), we know that Prosper changed the way they assess credit risk after 2008. I wanted to explore how loans changed at this time as well as look at whether the change improved Prosper's ability to predict bad loans. I chose a couple of boxplots and a scatterplot to highlight this because I felt they best showed how loans changed at that time. I finished my story with a line chart showing defaults and charge-offs over time, which suggested a reduction in defaults and charge-offs after 2008.

After receiving feedback on my initial story, I changed the tone of the captions, making them less chatty and tried to reduce wordiness. Also, I made the charts more interactive, including highlights and filters in each one, allowing viewers to explore the data on their own. I also added important information to a few of the charts to help make the story a little more clear.

For example, I added the line chart in the first dashboard, the one that tracks the number of loans over time in each state. I set the map to be a filter so that when the viewer hovers over a state on the map, the line chart will filter for that state. In addition, I included a reference line in the boxplots to help viewers see how loans changed after 2008. Finally, in the last chart, as one of the tooltips, I added the ratio of defaults and charge-offs to total loans so that viewers could see to what degree the credit risk assessment had improved.  

## Feedback
The feedback I received concerned the language in captions and the lack of interactivity in charts. Specifically, reviewers suggested that my tone was too chatty and that I was too wordy. I had included lines such as, "Let's start with some basics" and "We'll come back to that issue in a bit." Reviewers felt that tone was not fitting for a business-like review of data. Furthermore, reviewers felt that I was inserting my opinion in captions more so than allowing the data to do the explaining.

With regard to the charts, reviewers said there simply was not enough interactivity and not enough overall information. I had very few storyboards that used highlighters and filters. I had missed including interesting information in the demographics section, such as the change in loans over time broken down by state. And finally, on the last chart, I had not included the ratio of defaults and charge-offs to overall loans, making it nearly impossible to assess the effectiveness of Prosper's change in credit risk assessment.

## Resources
1. [Stackoverflow.com](www.stackoverflow.com)
2. [Tableau Help](http://onlinehelp.tableau.com/current/pro/desktop/en-us/help.htm#default.html%3FTocPath%3D_____1)
