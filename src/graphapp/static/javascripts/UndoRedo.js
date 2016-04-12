/*Olin Graph Program Spring 2016
**Authors: Josh Langowitz
**
**Class for registering events for undo and redo.
*/


/* Constructor
**
*/
function UndoRedo () {
    if (this instanceof UndoRedo) {
        this.stack = [];
        this.position = 0;
    } else {
        return new UndoRedo();
    }
}

/* Redoes a registered action
**
*/
UndoRedo.prototype.redo = function() {
    if (!this.hasRedo()) {
        throw new Error("There is nothing to redo, please check hasRedo before calling redo!");
    };
    return this.stack[this.position++](true);
};

/* Undoes a registered action
**
*/
UndoRedo.prototype.undo = function() {
    if (!this.hasUndo()) {
        throw new Error("There is nothing to undo, please check hasUndo before calling undo!");
    };
    return this.stack[--this.position](false);
};


/* Returns true if there is something to redo.
**
*/
UndoRedo.prototype.hasRedo = function() {
    return this.position < this.stack.length;
};

/* Returns true if there is something to undo.
**
*/
UndoRedo.prototype.hasUndo = function() {
    return this.position > 0;
};


/* Registers an action to undo or redo
** the undo redo function takes a boolean isRedo.
** It should perform a redo if that is true, otherwise an undo.
** It also should return a promise that is resolved when the undo or redo completes, in case it is async.
**
** fun - undo redo function
*/
UndoRedo.prototype.register = function(fun) {
    // Cut off any redoes past where we are now, then add this one.
    this.stack.splice(this.position);
    this.stack.push(fun);
    ++this.position;
};

