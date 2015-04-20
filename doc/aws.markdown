#Setting Up Coroner On AWS
Since Coroner is a data migration project we will need to run it on a shared resource and run backups after checkpoints are reached.

##Machines
Coroner is going to need to have Postgres installed on a ebs volume for easy backup and mirrors_server installed such that the django shell can be accessed.

Two machines should be sufficient for this and the Postgres server can be shared with any instances of mirrors we have running so once articles and authors are imported we can view them from a live instance of smoke/mirrors.

### Postgres Machine
Amazon offers RDS for Postgres supporting versions 9.3.X this includes backups and failover.  This seems like the fastest and most stable route to postgres on AWS and we be a good way to see how it works in production.

##Coroner Staging Machine
This machine needs to store json and binary data while its being collated out of the drupal database.  It will have mirrors_server installed on it including HTTP server so that we call view the imported components and pointed at the postgres machine.

In our case a t2.medium should suffice. All of the data stored on this server should be put on an EBS volume which is backed up whenever successful builds/migrations happen.  Whenever we are not actively migrating the server can be turned off and the EBS unmounted and put into storage for use later.

This machine needs to also have an ssh tunnel open to the drupal mysql database.  We should try and make sure its a read only access account for security reasons.

##Extra
* Smoke can either just run on the coroner server so that content can be viewed/edited live.
* Discuss if any automation of db migrations and continuous deployment.
