# Allow the server to startup
sleep 10

# Copy flaskapp.service
sudo cp flaskapp.service /etc/systemd/system/flaskapp.service

# Reload systemctl
sudo chmod 700 /etc/systemd/system/flaskapp.service
sudo systemctl daemon-reload

# Install Python and Postgres server
sudo yum update
sudo yum install python3

# Unzip the build file
tar xvzf webservice-0.0.1.tar.gz

# Add path to the environment
export PATH=/home/ec2-user/.local/bin:$PATH
#export S3_BUCKET="flask-s3-demo-dh"
#export S3_URL_PREFIX="flask-s3-demo-dh.s3.us-east-2.amazonaws.com"
#export RDS_USERNAME="admin"
#export RDS_DB="csye6225"

# Install dependencies
pip3 install python-dotenv
pip3 install -r requirements.txt
pip3 install -e webservice-0.0.1

# Run the application
sudo systemctl enable flaskapp.service
sudo systemctl status flaskapp.service
sudo systemctl start flaskapp.service