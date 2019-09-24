# docker, non-premium tutorials from Real Python

## [How to Make a Twitter Bot in Python With Tweepy][1]
by [Miguel Garcia][2] on Mon, 10 Jun 2019 with tags: [api][3], [docker][4], [intermediate][5] ([52 comments][6])

In this article, you’ll learn how to make your own Twitter Bot in Python with Tweepy, a package that provides a very convenient way to use the Twitter API.

Twitter is one of the most widely used social networks. For many organizations and people, having a great Twitter presence is a key factor to keeping their audience engaged.

Part of having a great Twitter presence involves keeping your account active with new tweets and retweets, following interesting accounts, and quickly replying to your followers’ messages. You can do all this work manually, but that can take a lot of time. Instead, you can rely on a __Twitter Bot__, a program that automates all or part of your Twitter activity.

__In this article, you’ll learn how to:__

*   Improve and automate your interactions with your Twitter audience
*   Install Tweepy
*   Sign up as a Twitter developer to use its API
*   Use Tweepy to invoke the Twitter API
*   Build Twitter Bots
*   Deploy the bots to a server using Docker and AWS

[1]: https://realpython.com/twitter-bot-python-tweepy/
[2]: https://realpython.com/twitter-bot-python-tweepy/#author
[3]: https://realpython.com/tutorials/api/
[4]: https://realpython.com/tutorials/docker/
[5]: https://realpython.com/tutorials/intermediate/
[6]: https://realpython.com/twitter-bot-python-tweepy/#reader-comments


## [Simplifying Offline Python Deployments With Docker][7]
by [Michael Herman][8] with tags: [devops][9], [docker][10], [intermediate][11], [python][12] ([4 comments][13])

In cases when a production server does not have access to the Internet or to the internal network, you will need to bundle up the Python dependencies (as wheel files) and interpreter along with the source code.

This post looks at how to package up a Python project for distribution internally on a machine cut off from the Internet [using Docker.](https://realpython.com/docker-in-action-fitter-happier-more-productive/)

[7]: https://realpython.com/offline-python-deployments-with-docker/
[8]: https://realpython.com/offline-python-deployments-with-docker/#author
[9]: https://realpython.com/tutorials/devops/
[10]: https://realpython.com/tutorials/docker/
[11]: https://realpython.com/tutorials/intermediate/
[12]: https://realpython.com/tutorials/python/
[13]: https://realpython.com/offline-python-deployments-with-docker/#reader-comments


## [Development and Deployment of Cookiecutter-Django via Docker][14]
by [Real Python][15] with tags: [devops][16], [django][17], [docker][18], [web-dev][19] ([66 comments][20])

__Let’s look at how to bootstrap a Django Project pre-loaded with the basic requirements needed in order to quickly get a project up and running.__ Further, beyond the project structure, most bootstrapped projects also take care of setting up the development and production environment settings, without troubling the user much - so we’ll look at that as well.

__Updates__:

*   
    
    _04/15/2019_: Updated to the latest versions of cookiecutter (v[1.6.0](https://github.com/audreyr/cookiecutter/releases/tag/1.6.0)), cookiecutter-django, Django (v[2.0](https://docs.djangoproject.com/en/2.2/)), Docker (v[18.09.2](https://github.com/docker/docker-ce/releases/tag/v18.09.2)), Docker Compose (v[1.23.2](https://github.com/docker/compose/releases/tag/1.23.2)), and Docker Machine (v[0.16.1](https://github.com/docker/machine/releases/tag/v0.16.1)).
    
    
*   
    
    _10/04/2016_: Updated to the latest versions of cookiecutter (v[1.4.0](https://github.com/audreyr/cookiecutter/releases/tag/1.4.0)), cookiecutter-django, Django (v[1.10.1](https://docs.djangoproject.com/en/1.10/releases/1.10.1/)), Docker (v[1.12.1](https://github.com/docker/docker/releases/tag/v1.12.1)), Docker Compose (v[1.8.1](https://github.com/docker/compose/releases/tag/1.8.1)), and Docker Machine (v[0.8.2](https://github.com/docker/machine/releases/tag/v0.8.2)).
    
    

We’ll be using the popular [cookiecutter-django](https://github.com/pydanny/cookiecutter-django) as the bootstrapper for our Django Project along with [Docker](https://www.docker.com/) to manage our application environment.

Let’s begin!

[14]: https://realpython.com/development-and-deployment-of-cookiecutter-django-via-docker/
[15]: https://realpython.com/development-and-deployment-of-cookiecutter-django-via-docker/#team
[16]: https://realpython.com/tutorials/devops/
[17]: https://realpython.com/tutorials/django/
[18]: https://realpython.com/tutorials/docker/
[19]: https://realpython.com/tutorials/web-dev/
[20]: https://realpython.com/development-and-deployment-of-cookiecutter-django-via-docker/#reader-comments


## [Django Development with Docker Compose and Machine][21]
by [Real Python][22] with tags: [advanced][23], [devops][24], [django][25], [docker][26], [web-dev][27] ([199 comments][28])

[Docker](https://www.docker.com/) is a containerization tool used for spinning up isolated, reproducible application environments. __This piece details how to containerize a Django Project, Postgres, and Redis for local development along with delivering the stack to the cloud via [Docker Compose](https://docs.docker.com/compose/) and [Docker Machine](http://docs.docker.com/machine/).__

[21]: https://realpython.com/django-development-with-docker-compose-and-machine/
[22]: https://realpython.com/django-development-with-docker-compose-and-machine/#team
[23]: https://realpython.com/tutorials/advanced/
[24]: https://realpython.com/tutorials/devops/
[25]: https://realpython.com/tutorials/django/
[26]: https://realpython.com/tutorials/docker/
[27]: https://realpython.com/tutorials/web-dev/
[28]: https://realpython.com/django-development-with-docker-compose-and-machine/#reader-comments


## [Dockerizing Flask With Compose and Machine – From Localhost to the Cloud][29]
by [Real Python][30] with tags: [advanced][31], [devops][32], [docker][33], [flask][34], [web-dev][35] ([92 comments][36])

[Docker](https://www.docker.com/) is a powerful tool for spinning up isolated, reproducible application environment _containers_. __This piece looks at just that—how to containerize a Flask app for local development along with delivering the application to a cloud hosting provider via Docker Compose and Docker Machine.__

_Updates:_

*   03/31/2019: Updated to the latest versions of Docker - Docker client (v18.09.2), Docker compose (v1.23.2), and Docker Machine (v0.16.1) Thanks [Florian Dahlitz](https://github.com/DahlitzFlorian)!
*   11/16/2015: Updated to the latest versions of Docker - Docker client (v1.9.0), Docker compose (v1.5.0), and Docker Machine (v0.5.0)
*   04/25/2015: Fixed small typo, and updated the _docker-compose.yml_ file to properly copy static files.
*   04/19/2015: Added a shell script for copying static files.

>  
> Interested in creating a similar environment for Django? Check out [this](https://realpython.com/django-development-with-docker-compose-and-machine/) blog post.
> 

[29]: https://realpython.com/dockerizing-flask-with-compose-and-machine-from-localhost-to-the-cloud/
[30]: https://realpython.com/dockerizing-flask-with-compose-and-machine-from-localhost-to-the-cloud/#team
[31]: https://realpython.com/tutorials/advanced/
[32]: https://realpython.com/tutorials/devops/
[33]: https://realpython.com/tutorials/docker/
[34]: https://realpython.com/tutorials/flask/
[35]: https://realpython.com/tutorials/web-dev/
[36]: https://realpython.com/dockerizing-flask-with-compose-and-machine-from-localhost-to-the-cloud/#reader-comments


## [Docker in Action – Fitter, Happier, More Productive][37]
by [Real Python][38] with tags: [devops][39], [docker][40], [flask][41], [web-dev][42] ([31 comments][43])

With Docker you can easily deploy a web application along with it’s dependencies, environment variables, and configuration settings - everything you need to recreate your environment quickly and efficiently.

This tutorial looks at just that.

__We’ll start by creating a Docker container for running a Python Flask application. From there, we’ll look at a nice development workflow to manage the local development of an app as well as continuous integration and delivery, step by step …__

>  
> I ([Michael Herman](https://twitter.com/mikeherman)) originally presented this workflow at [ PyTennessee](https://www.pytennessee.org/) on February 8th, 2015. You can view the slides [here](http://realpython.github.io/fitter-happier-docker/), if interested.
> 

__Updated 04/04/2019__: Upgraded Docker (v18.09.2), Docker Compose (v1.23.2), Docker Machine (v0.16.1), Python (v3.7.3), and CircleCI (v2). Thanks [Florian Dahlitz](https://github.com/DahlitzFlorian)!

__Updated 02/28/2015__: Added [Docker Compose](https://docs.docker.com/compose/) and upgraded Docker and boot2docker to the latest versions.

[37]: https://realpython.com/docker-in-action-fitter-happier-more-productive/
[38]: https://realpython.com/docker-in-action-fitter-happier-more-productive/#team
[39]: https://realpython.com/tutorials/devops/
[40]: https://realpython.com/tutorials/docker/
[41]: https://realpython.com/tutorials/flask/
[42]: https://realpython.com/tutorials/web-dev/
[43]: https://realpython.com/docker-in-action-fitter-happier-more-productive/#reader-comments


## [Deploying Django on Dokku][44]
by [Real Python][45] with tags: [advanced][46], [devops][47], [django][48], [docker][49], [web-dev][50] ([5 comments][51])

Originally written for _[Gun.io](http://www.gun.io)_, this post details how to use Dokku as a Heroku replacement for deploying your Django App.

[44]: https://realpython.com/deploying-a-django-app-on-dokku/
[45]: https://realpython.com/
[46]: https://realpython.com/tutorials/advanced/
[47]: https://realpython.com/tutorials/devops/
[48]: https://realpython.com/tutorials/django/
[49]: https://realpython.com/tutorials/docker/
[50]: https://realpython.com/tutorials/web-dev/
[51]: https://realpython.com/deploying-a-django-app-on-dokku/#reader-comments


## [Twitter Sentiment Analysis – Python, Docker, Elasticsearch, Kibana][52]
by [Real Python][53] with tags: [advanced][54], [api][55], [data-science][56], [docker][57], [web-dev][58] ([61 comments][59])

In this example, we’ll connect to the Twitter Streaming API, gather tweets (based on a keyword), [calculate the sentiment](https://realpython.com/python-keras-text-classification/) of each tweet, and build a real-time dashboard using the Elasticsearch DB and Kibana to visualize the results.

>  
> Tools: [Docker](https://www.docker.com/) v1.3.0, [boot2docker](http://boot2docker.io/) v1.3.0, [Tweepy](http://www.tweepy.org/) v2.3.0, [TextBlob](http://textblob.readthedocs.org/en/dev/) v0.9.0, [Elasticsearch](http://www.elasticsearch.org/) v1.3.5, [Kibana](http://www.elasticsearch.org/overview/kibana/) v3.1.2
> 

[52]: https://realpython.com/twitter-sentiment-python-docker-elasticsearch-kibana/
[53]: https://realpython.com/
[54]: https://realpython.com/tutorials/advanced/
[55]: https://realpython.com/tutorials/api/
[56]: https://realpython.com/tutorials/data-science/
[57]: https://realpython.com/tutorials/docker/
[58]: https://realpython.com/tutorials/web-dev/
[59]: https://realpython.com/twitter-sentiment-python-docker-elasticsearch-kibana/#reader-comments


