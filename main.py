from conf import app,connex_app

connex_app.add_api("open_api/swagger.yml")

if __name__ == '__main__':
    app.app_context().push()
    # db.drop_all()
    # db.create_all()

    app.run(host="0.0.0.0", port=8000, debug=True)
