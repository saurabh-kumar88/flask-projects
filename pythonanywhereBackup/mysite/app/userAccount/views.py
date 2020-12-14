from flask import render_template, abort, flash

from . import userAccount


@userAccount.route('/account')
def account():
    account_msg = "Coming Soon...........!!"
    return render_template('admin/index.html', account_msg=account_msg)


@userAccount.route('/favorites')
def favorites():
    favorites_msg = "Favorites coming Soon...........!!"
    return render_template('admin/index.html', favorites_msg=favorites_msg)

@userAccount.route('/service')
def service():
    service_msg = "Services coming Soon...........!!"
    return render_template('admin/index.html', service_msg=service_msg)

@userAccount.route('/settings')
def settings():
    setting_msg = "Settings coming Soon...........!!"
    return render_template('admin/index.html', setting_msg=setting_msg)