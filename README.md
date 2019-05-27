## Trend identification and estimation in time series

Student(s): Grillo, A., Hanrieder, M., Mauranen, H., Mikos, M., Wiezorek, J.  
Supervisor(s): Bonizzi, P.  
Semester: 2018-2019

![Fig 1. - How a trend can affect the
interpretation](website/images/Components.png)

#### Background

This project should help to analyse time series data, which is a special
type of data with a time-value, such as seconds or timestamp, as x-value
and any observed value as y-value. The y-value can then be a measured
value like temperature or stock exchange data. In a mathematical sense
this kind of data consists of several components. One component is the
so-called noise which describes random events or measurement errors.
Another component is the season, such as time of year in weather data.
In general the season component describes repetitive behaviour during
the observation period. Furthermore, data can contain a trend, which
describes how the data will develop beyond the measurement period. In
Fig. 1 a synthetic time series data was generated with these three
different components, a trend, random noise and seasonality.

A main topic of this project is to find trends, which can be split in
two parts. The first part is the identification, which means finding out
if a trend exists, while the second part is to estimate this trend. An
estimation of a trend can be an equation like *x+5* or just a list of
points. This depends on the method that is used. Trends can have
different shapes such as just a straight increasing or decreasing line
or more complex curves like simple polynomials. An overview about the
considered types of trend can be found in Fig 2. Different methods can
either identify or estimate a trend, or do both.

![Fig 2. - Performance analysis on monotonic trend](website/images/Rplot.png)

#### Problem statement and motivation

It is very useful to separate the trend and season from the time series.
For instance, scientists investigating global warming are interested in
the overall changes, or trend, in temperature and not so much in the
seasonal changes. Another example application is medicine, where
electrocardiograms suffer from patient's breathing and baseline wander,
that cause the heartbeats to be shifted away. There it is more useful to
consider the series without the long-term changes. The quality of the
separation for each component allows easier analysis on the time series.

There are multiple ways to take apart time series recordings. However,
none of them are considered the standard way and little research exists
to compare the methods for different types of time series. Our goal is
to systematically compare the different approaches to find the best one
or to be able to give the best method for specific type of time series.

#### Methods

A lot of methods are able to detect or approximate a trend, but these
methods perform differently depending on the influences of the trend,
the seasonal component and the noise. Mostly common methods, such as
regression, are covered with a couple more complex methods. An overview
and a brief description of them can be found in the report. All of the
methods are applied to each trend individually. This allows determining
the best method for a trend type. These results are compared to find
either the best overall method or a group of trends where specific
methods perform well.

An example analysis of the estimation methods on two different trends
can be found in Fig 3 and Fig 4, in the bar chart on the right the
distance to the original trend is measured, so the smaller the value,
the better the performance. On the mixed polynomial trend most methods
perform very well, but the Theil-Sen estimator performs very bad. While
on the monotonic trend all methods performs comparable except for the
discrete wavelet spectrum which performs worse.

![Fig 3. - Performance analysis on mixed polynomial
trend](website/images/methods_1.png)

![Fig 4. - Performance analysis on monotonic
trend](website/images/methods_2.png)

#### Research questions

  - What are the best and most versatile approaches for trend
    identification and estimation in time series data?
  - What are the strengths and weak points of the different methods
    tested?
  - Is it possible to automatically select the best approach(es) for
    trend identification and estimation, based on the
    (statistical/frequency/etc.) properties of a time series and the
    specific problem domain and application?

#### Main outcome

The research results in the comparison of strengths and weaknesses of
different methods for trend detection and estimation.

#### Downloads:

[Final report](”???”) [Final presentation](”???”)
