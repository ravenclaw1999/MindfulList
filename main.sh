touch ~/.customize_environment
echo 'sudo pip3 install flask' >> ~/.customize_environment
echo 'sudo pip3 install python-dotenv' >> ~/.customize_environment

export FLASK_APP=app.py
export FLASK_DEBUG=1

python -m flask run --host=0.0.0.0