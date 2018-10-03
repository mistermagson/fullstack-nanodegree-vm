from flask import Flask, render_template, request, redirect,jsonify, url_for, flash
app = Flask(__name__)

from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Category, Item


#Connect to Database and create database session
engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


#JSON APIs to view Category Information
@app.route('/category/<int:category_id>/items/JSON')
def CategoryMenuJSON(category_id):
    category = session.query(Category).filter_by(id = category_id).one()
    items = session.query(Item).filter_by(category_id = category_id).all()
    return jsonify(Items=[i.serialize for i in items])


@app.route('/category/<int:category_id>/item/<int:item_id>/JSON')
def menuItemJSON(category_id, item):
    Menu_Item = session.query(MenuItem).filter_by(id = menu_id).one()
    return jsonify(Menu_Item = Menu_Item.serialize)

@app.route('/category/JSON')
def CategoriesJSON():
    categories = session.query(Category).all()
    return jsonify(Categories= [r.serialize for r in categories])


#Show all Categories
@app.route('/')
@app.route('/category/')
def showCategories():
  categories = session.query(Category).order_by(asc(Category.name))
  items = session.query(Item).limit(2).all()
  return render_template('categories.html', categories = categories, items=items)

#Create a new Category
@app.route('/category/new/', methods=['GET','POST'])
def newCategory():
  if request.method == 'POST':
      newCategory = Category(name = request.form['name'])
      session.add(newCategory)
      flash('New Category %s Successfully Created' % newCategory.name)
      session.commit()
      return redirect(url_for('showCategories'))
  else:
      return render_template('newCategory.html')

#Edit a Category
@app.route('/category/<int:category_id>/edit/', methods = ['GET', 'POST'])
def editCategory(category_id):
  editedCategory = session.query(Category).filter_by(id = category_id).one()
  if request.method == 'POST':
      if request.form['name']:
        editedCategory.name = request.form['name']
        flash('Category Successfully Edited %s' % editedCategory.name)
        session.commit()
        return redirect(url_for('showCategories'))
  else:
    return render_template('editCategory.html', category = editedCategory)


#Delete a Category
@app.route('/category/<int:category_id>/delete/', methods = ['GET','POST'])
def deleteCategory(category_id):
  categoryToDelete = session.query(Category).filter_by(id = category_id).one()
  if request.method == 'POST':
    session.delete(categoryToDelete)
    flash('%s Successfully Deleted' % CategoryToDelete.name)
    session.commit()
    return redirect(url_for('showCategories', category_id = category_id))
  else:
    return render_template('deleteCategory.html',Category = CategoryToDelete)

#Show a Category menu
@app.route('/category/<int:category_id>/')
@app.route('/category/<int:category_id>/menu/')
def showItems(category_id):
    category = session.query(Category).filter_by(id = category_id).one()
    items = session.query(Item).filter_by(category_id = category_id).all()
    return render_template('category.html', items = items, category = category)

@app.route('/category/<int:category_id>/<int:item_id>/show')
def showItem(item_id):
    item = session.query(Item).filter_by(id = item_id).one()
    return render_template('menu.html', item = item)

#Create a new menu item
@app.route('/category/<int:category_id>/item/new/',methods=['GET','POST'])
def newItem(category_id):
  category = session.query(Category).filter_by(id = category_id).one()
  if request.method == 'POST':
      newItem = Item(title = request.form['title'], description = request.form['description'], category= category)
      session.add(newItem)
      session.commit()
      flash('New Menu %s Item Successfully Created' % (newItem.name))
      return redirect(url_for('showMenu', category_id = category_id))
  else:
      return render_template('newcategoryitem.html', category_id = category_id)

#Edit a menu item
@app.route('/category/<int:category_id>/item/<int:item_id>/edit', methods=['GET','POST'])
def editItem(category_id, item_id):
    editedItem = session.query(Item).filter_by(id = item_id).one()
    category = session.query(Category).filter_by(id = category_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['description']
        session.add(editedItem)
        session.commit()
        flash('Category Item Successfully Edited')
        return redirect(url_for('showItems', category_id = category_id))
    else:
        return render_template('editcategoryitem.html', category_id = category_id, item = editedItem)


#Delete a menu item
@app.route('/category/<int:category_id>/item/<int:item_id>/delete', methods = ['GET','POST'])
def deleteItem(category_id,item_id):
    category = session.query(Category).filter_by(id = category_id).one()
    itemToDelete = session.query(Item).filter_by(id = item_id).one()
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash('Category Item Successfully Deleted')
        return redirect(url_for('showCategories', category_id = category_id))
    else:
        return render_template('deleteItem.html', item = itemToDelete)




if __name__ == '__main__':
  app.secret_key = 'super_secret_key'
  app.debug = True
  app.run(host = '0.0.0.0', port = 5000)
