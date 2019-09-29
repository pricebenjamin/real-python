# docker tutorials and courses from Real Python

## [How to Make a Twitter Bot in Python With Tweepy](https://realpython.com/twitter-bot-python-tweepy/)

by [Miguel Garcia](https://realpython.com/twitter-bot-python-tweepy/#author) on Mon, 10 Jun 2019 with tags: [api](https://realpython.com/tutorials/api/), [docker](https://realpython.com/tutorials/docker/), [intermediate](https://realpython.com/tutorials/intermediate/) ([52 comments](https://realpython.com/twitter-bot-python-tweepy/#reader-comments))

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

## [Simplifying Offline Python Deployments With Docker](https://realpython.com/offline-python-deployments-with-docker/)

by [Michael Herman](https://realpython.com/offline-python-deployments-with-docker/#author) with tags: [devops](https://realpython.com/tutorials/devops/), [docker](https://realpython.com/tutorials/docker/), [intermediate](https://realpython.com/tutorials/intermediate/), [python](https://realpython.com/tutorials/python/) ([4 comments](https://realpython.com/offline-python-deployments-with-docker/#reader-comments))

In cases when a production server does not have access to the Internet or to the internal network, you will need to bundle up the Python dependencies (as wheel files) and interpreter along with the source code.

This post looks at how to package up a Python project for distribution internally on a machine cut off from the Internet [using Docker.](https://realpython.com/docker-in-action-fitter-happier-more-productive/)

## [Development and Deployment of Cookiecutter-Django via Docker](https://realpython.com/development-and-deployment-of-cookiecutter-django-via-docker/)

by [Real Python](https://realpython.com/development-and-deployment-of-cookiecutter-django-via-docker/#team) with tags: [devops](https://realpython.com/tutorials/devops/), [django](https://realpython.com/tutorials/django/), [docker](https://realpython.com/tutorials/docker/), [web-dev](https://realpython.com/tutorials/web-dev/) ([66 comments](https://realpython.com/development-and-deployment-of-cookiecutter-django-via-docker/#reader-comments))

__Let’s look at how to bootstrap a Django Project pre-loaded with the basic requirements needed in order to quickly get a project up and running.__ Further, beyond the project structure, most bootstrapped projects also take care of setting up the development and production environment settings, without troubling the user much - so we’ll look at that as well.

__Updates__:

*   
    
    _04/15/2019_: Updated to the latest versions of cookiecutter (v[1.6.0](https://github.com/audreyr/cookiecutter/releases/tag/1.6.0)), cookiecutter-django, Django (v[2.0](https://docs.djangoproject.com/en/2.2/)), Docker (v[18.09.2](https://github.com/docker/docker-ce/releases/tag/v18.09.2)), Docker Compose (v[1.23.2](https://github.com/docker/compose/releases/tag/1.23.2)), and Docker Machine (v[0.16.1](https://github.com/docker/machine/releases/tag/v0.16.1)).
    
    
*   
    
    _10/04/2016_: Updated to the latest versions of cookiecutter (v[1.4.0](https://github.com/audreyr/cookiecutter/releases/tag/1.4.0)), cookiecutter-django, Django (v[1.10.1](https://docs.djangoproject.com/en/1.10/releases/1.10.1/)), Docker (v[1.12.1](https://github.com/docker/docker/releases/tag/v1.12.1)), Docker Compose (v[1.8.1](https://github.com/docker/compose/releases/tag/1.8.1)), and Docker Machine (v[0.8.2](https://github.com/docker/machine/releases/tag/v0.8.2)).
    
    

We’ll be using the popular [cookiecutter-django](https://github.com/pydanny/cookiecutter-django) as the bootstrapper for our Django Project along with [Docker](https://www.docker.com/) to manage our application environment.

Let’s begin!

## [Django Development with Docker Compose and Machine](https://realpython.com/django-development-with-docker-compose-and-machine/)

by [Real Python](https://realpython.com/django-development-with-docker-compose-and-machine/#team) with tags: [advanced](https://realpython.com/tutorials/advanced/), [devops](https://realpython.com/tutorials/devops/), [django](https://realpython.com/tutorials/django/), [docker](https://realpython.com/tutorials/docker/), [web-dev](https://realpython.com/tutorials/web-dev/) ([199 comments](https://realpython.com/django-development-with-docker-compose-and-machine/#reader-comments))

[Docker](https://www.docker.com/) is a containerization tool used for spinning up isolated, reproducible application environments. __This piece details how to containerize a Django Project, Postgres, and Redis for local development along with delivering the stack to the cloud via [Docker Compose](https://docs.docker.com/compose/) and [Docker Machine](http://docs.docker.com/machine/).__

## [Dockerizing Flask With Compose and Machine – From Localhost to the Cloud](https://realpython.com/dockerizing-flask-with-compose-and-machine-from-localhost-to-the-cloud/)

by [Real Python](https://realpython.com/dockerizing-flask-with-compose-and-machine-from-localhost-to-the-cloud/#team) with tags: [advanced](https://realpython.com/tutorials/advanced/), [devops](https://realpython.com/tutorials/devops/), [docker](https://realpython.com/tutorials/docker/), [flask](https://realpython.com/tutorials/flask/), [web-dev](https://realpython.com/tutorials/web-dev/) ([92 comments](https://realpython.com/dockerizing-flask-with-compose-and-machine-from-localhost-to-the-cloud/#reader-comments))

[Docker](https://www.docker.com/) is a powerful tool for spinning up isolated, reproducible application environment _containers_. __This piece looks at just that—how to containerize a Flask app for local development along with delivering the application to a cloud hosting provider via Docker Compose and Docker Machine.__

_Updates:_

*   03/31/2019: Updated to the latest versions of Docker - Docker client (v18.09.2), Docker compose (v1.23.2), and Docker Machine (v0.16.1) Thanks [Florian Dahlitz](https://github.com/DahlitzFlorian)!
*   11/16/2015: Updated to the latest versions of Docker - Docker client (v1.9.0), Docker compose (v1.5.0), and Docker Machine (v0.5.0)
*   04/25/2015: Fixed small typo, and updated the _docker-compose.yml_ file to properly copy static files.
*   04/19/2015: Added a shell script for copying static files.

>  
> Interested in creating a similar environment for Django? Check out [this](https://realpython.com/django-development-with-docker-compose-and-machine/) blog post.
> 

## [Docker in Action – Fitter, Happier, More Productive](https://realpython.com/docker-in-action-fitter-happier-more-productive/)

by [Real Python](https://realpython.com/docker-in-action-fitter-happier-more-productive/#team) with tags: [devops](https://realpython.com/tutorials/devops/), [docker](https://realpython.com/tutorials/docker/), [flask](https://realpython.com/tutorials/flask/), [web-dev](https://realpython.com/tutorials/web-dev/) ([31 comments](https://realpython.com/docker-in-action-fitter-happier-more-productive/#reader-comments))

With Docker you can easily deploy a web application along with it’s dependencies, environment variables, and configuration settings - everything you need to recreate your environment quickly and efficiently.

This tutorial looks at just that.

__We’ll start by creating a Docker container for running a Python Flask application. From there, we’ll look at a nice development workflow to manage the local development of an app as well as continuous integration and delivery, step by step …__

>  
> I ([Michael Herman](https://twitter.com/mikeherman)) originally presented this workflow at [ PyTennessee](https://www.pytennessee.org/) on February 8th, 2015. You can view the slides [here](http://realpython.github.io/fitter-happier-docker/), if interested.
> 

__Updated 04/04/2019__: Upgraded Docker (v18.09.2), Docker Compose (v1.23.2), Docker Machine (v0.16.1), Python (v3.7.3), and CircleCI (v2). Thanks [Florian Dahlitz](https://github.com/DahlitzFlorian)!

__Updated 02/28/2015__: Added [Docker Compose](https://docs.docker.com/compose/) and upgraded Docker and boot2docker to the latest versions.

## [Deploying Django on Dokku](https://realpython.com/deploying-a-django-app-on-dokku/)

by [Real Python](https://realpython.com/) with tags: [advanced](https://realpython.com/tutorials/advanced/), [devops](https://realpython.com/tutorials/devops/), [django](https://realpython.com/tutorials/django/), [docker](https://realpython.com/tutorials/docker/), [web-dev](https://realpython.com/tutorials/web-dev/) ([5 comments](https://realpython.com/deploying-a-django-app-on-dokku/#reader-comments))

Originally written for _[Gun.io](http://www.gun.io)_, this post details how to use Dokku as a Heroku replacement for deploying your Django App.

## [Twitter Sentiment Analysis – Python, Docker, Elasticsearch, Kibana](https://realpython.com/twitter-sentiment-python-docker-elasticsearch-kibana/)

by [Real Python](https://realpython.com/) with tags: [advanced](https://realpython.com/tutorials/advanced/), [api](https://realpython.com/tutorials/api/), [data-science](https://realpython.com/tutorials/data-science/), [docker](https://realpython.com/tutorials/docker/), [web-dev](https://realpython.com/tutorials/web-dev/) ([61 comments](https://realpython.com/twitter-sentiment-python-docker-elasticsearch-kibana/#reader-comments))

In this example, we’ll connect to the Twitter Streaming API, gather tweets (based on a keyword), [calculate the sentiment](https://realpython.com/python-keras-text-classification/) of each tweet, and build a real-time dashboard using the Elasticsearch DB and Kibana to visualize the results.

>  
> Tools: [Docker](https://www.docker.com/) v1.3.0, [boot2docker](http://boot2docker.io/) v1.3.0, [Tweepy](http://www.tweepy.org/) v2.3.0, [TextBlob](http://textblob.readthedocs.org/en/dev/) v0.9.0, [Elasticsearch](http://www.elasticsearch.org/) v1.3.5, [Kibana](http://www.elasticsearch.org/overview/kibana/) v3.1.2
> 

