### Here is a list of routes used in app for reference: 


# complaints

* '/complaints' 
   - methods: get, post, delete, patch 
   - on get, lists all complaints in database.
   - do not extend with queries i.e 'complaints/?name=bruh', will not work

* 'list/complaint/user/<email>'
   - methods: get 
   - gets all complaints for user with email equal to <email>

* 'complaint/user'
   - method: get
   - can be extended with queries

# users

* '/user/<id>'
   - methods: get, delete, patch
   - will list user number id in database (id is differentf from '_id')
   - do not extend with queries

* '/user'
   - methods: get, delete, patch
   - can be extended with queries

* 'register/'
- methods: post 
- will create new user : (required: email, password)

* '/auth'
   - methods: post
   - to authenticate user.

* '/refresh'
   - keeps track of current user.

# note

* '/notes'
  - methods: get, post 
  - can be extended with queries
  - list notes as query specifies



# see schemas folder for the expected schemas and required fields!