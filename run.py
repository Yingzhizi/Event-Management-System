from server import app

if __name__ == '__main__':
    app.secret_key = 'wobuffet'
    app.run(debug=True)
