# docker, non-premium tutorials from Real Python

### [How to Make a Twitter Bot in Python With Tweepy](https://realpython.com/twitter-bot-python-tweepy/)

> <p>In this article, you’ll learn how to make your own Twitter Bot in Python with Tweepy, a package that provides a very convenient way to use the Twitter API.</p>
> <p>Twitter is one of the most widely used social networks. For many organizations and people, having a great Twitter presence is a key factor to keeping their audience engaged.</p>
> <p>Part of having a great Twitter presence involves keeping your account active with new tweets and retweets, following interesting accounts, and quickly replying to your followers’ messages. You can do all this work manually, but that can take a lot of time. Instead, you can rely on a <strong>Twitter Bot</strong>, a program that automates all or part of your Twitter activity.</p>
> <p><strong>In this article, you’ll learn how to:</strong></p>
> <ul>
> <li>Improve and automate your interactions with your Twitter audience</li>
> <li>Install Tweepy</li>
> <li>Sign up as a Twitter developer to use its API</li>
> <li>Use Tweepy to invoke the Twitter API</li>
> <li>Build Twitter Bots</li>
> <li>Deploy the bots to a server using Docker and AWS</li>
> </ul>

### [Simplifying Offline Python Deployments With Docker](https://realpython.com/offline-python-deployments-with-docker/)

> <p>In cases when a production server does not have access to the Internet or to the internal network, you will need to bundle up the Python dependencies (as wheel files) and interpreter along with the source code.</p>
> <p>This post looks at how to package up a Python project for distribution internally on a machine cut off from the Internet <a href="https://realpython.com/docker-in-action-fitter-happier-more-productive/">using Docker.</a></p>

### [Development and Deployment of Cookiecutter-Django via Docker](https://realpython.com/development-and-deployment-of-cookiecutter-django-via-docker/)

> <p><strong>Let’s look at how to bootstrap a Django Project pre-loaded with the basic requirements needed in order to quickly get a project up and running.</strong> Further, beyond the project structure, most bootstrapped projects also take care of setting up the development and production environment settings, without troubling the user much - so we’ll look at that as well.</p>
> <p><strong>Updates</strong>:</p>
> <ul>
> <li>
> <p><em>04/15/2019</em>: Updated to the latest versions of cookiecutter (v<a href="https://github.com/audreyr/cookiecutter/releases/tag/1.6.0">1.6.0</a>), cookiecutter-django, Django (v<a href="https://docs.djangoproject.com/en/2.2/">2.0</a>), Docker (v<a href="https://github.com/docker/docker-ce/releases/tag/v18.09.2">18.09.2</a>), Docker Compose (v<a href="https://github.com/docker/compose/releases/tag/1.23.2">1.23.2</a>), and Docker Machine (v<a href="https://github.com/docker/machine/releases/tag/v0.16.1">0.16.1</a>).</p>
> </li>
> <li>
> <p><em>10/04/2016</em>: Updated to the latest versions of cookiecutter (v<a href="https://github.com/audreyr/cookiecutter/releases/tag/1.4.0">1.4.0</a>), cookiecutter-django, Django (v<a href="https://docs.djangoproject.com/en/1.10/releases/1.10.1/">1.10.1</a>), Docker (v<a href="https://github.com/docker/docker/releases/tag/v1.12.1">1.12.1</a>), Docker Compose (v<a href="https://github.com/docker/compose/releases/tag/1.8.1">1.8.1</a>), and Docker Machine (v<a href="https://github.com/docker/machine/releases/tag/v0.8.2">0.8.2</a>).</p>
> </li>
> </ul>
> <p>We’ll be using the popular <a href="https://github.com/pydanny/cookiecutter-django">cookiecutter-django</a> as the bootstrapper for our Django Project along with <a href="https://www.docker.com/">Docker</a> to manage our application environment.</p>
> <p>Let’s begin!</p>

### [Django Development with Docker Compose and Machine](https://realpython.com/django-development-with-docker-compose-and-machine/)

> <p><a href="https://www.docker.com/">Docker</a> is a containerization tool used for spinning up isolated, reproducible application environments. <strong>This piece details how to containerize a Django Project, Postgres, and Redis for local development along with delivering the stack to the cloud via <a href="https://docs.docker.com/compose/">Docker Compose</a> and <a href="http://docs.docker.com/machine/">Docker Machine</a>.</strong></p>

### [Dockerizing Flask With Compose and Machine – From Localhost to the Cloud](https://realpython.com/dockerizing-flask-with-compose-and-machine-from-localhost-to-the-cloud/)

> <p><a href="https://www.docker.com/">Docker</a> is a powerful tool for spinning up isolated, reproducible application environment <em>containers</em>. <strong>This piece looks at just that—how to containerize a Flask app for local development along with delivering the application to a cloud hosting provider via Docker Compose and Docker Machine.</strong></p>
> <p><em>Updates:</em></p>
> <ul>
> <li>03/31/2019: Updated to the latest versions of Docker - Docker client (v18.09.2), Docker compose (v1.23.2), and Docker Machine (v0.16.1) Thanks <a href="https://github.com/DahlitzFlorian">Florian Dahlitz</a>!</li>
> <li>11/16/2015: Updated to the latest versions of Docker - Docker client (v1.9.0), Docker compose (v1.5.0), and Docker Machine (v0.5.0)</li>
> <li>04/25/2015: Fixed small typo, and updated the <em>docker-compose.yml</em> file to properly copy static files.</li>
> <li>04/19/2015: Added a shell script for copying static files.</li>
> </ul>
> <blockquote>
> <p>Interested in creating a similar environment for Django? Check out <a href="https://realpython.com/django-development-with-docker-compose-and-machine/">this</a> blog post.</p>
> </blockquote>

### [Docker in Action – Fitter, Happier, More Productive](https://realpython.com/docker-in-action-fitter-happier-more-productive/)

> <p>With Docker you can easily deploy a web application along with it’s dependencies, environment variables, and configuration settings - everything you need to recreate your environment quickly and efficiently.</p>
> <p>This tutorial looks at just that.</p>
> <p><strong>We’ll start by creating a Docker container for running a Python Flask application. From there, we’ll look at a nice development workflow to manage the local development of an app as well as continuous integration and delivery, step by step …</strong></p>
> <blockquote>
> <p>I (<a href="https://twitter.com/mikeherman">Michael Herman</a>) originally presented this workflow at <a href="https://www.pytennessee.org/"> PyTennessee</a> on February 8th, 2015. You can view the slides <a href="http://realpython.github.io/fitter-happier-docker/">here</a>, if interested.</p>
> </blockquote>
> <p><strong>Updated 04/04/2019</strong>: Upgraded Docker (v18.09.2), Docker Compose (v1.23.2), Docker Machine (v0.16.1), Python (v3.7.3), and CircleCI (v2). Thanks <a href="https://github.com/DahlitzFlorian">Florian Dahlitz</a>!</p>
> <p><strong>Updated 02/28/2015</strong>: Added <a href="https://docs.docker.com/compose/">Docker Compose</a> and upgraded Docker and boot2docker to the latest versions.</p>

### [Deploying Django on Dokku](https://realpython.com/deploying-a-django-app-on-dokku/)

> <p>Originally written for <em><a href="http://www.gun.io">Gun.io</a></em>, this post details how to use Dokku as a Heroku replacement for deploying your Django App.</p>

### [Twitter Sentiment Analysis – Python, Docker, Elasticsearch, Kibana](https://realpython.com/twitter-sentiment-python-docker-elasticsearch-kibana/)

> <p>In this example, we’ll connect to the Twitter Streaming API, gather tweets (based on a keyword), <a href="https://realpython.com/python-keras-text-classification/">calculate the sentiment</a> of each tweet, and build a real-time dashboard using the Elasticsearch DB and Kibana to visualize the results.</p>
> <blockquote>
> <p>Tools: <a href="https://www.docker.com/">Docker</a> v1.3.0, <a href="http://boot2docker.io/">boot2docker</a> v1.3.0, <a href="http://www.tweepy.org/">Tweepy</a> v2.3.0, <a href="http://textblob.readthedocs.org/en/dev/">TextBlob</a> v0.9.0, <a href="http://www.elasticsearch.org/">Elasticsearch</a> v1.3.5, <a href="http://www.elasticsearch.org/overview/kibana/">Kibana</a> v3.1.2</p>
> </blockquote>

