"""
fleetdb.py - Python interface to FleetDB (http://fleetdb.org/)
 
Library Maintainer:  
    Matt Culbreth
    mattculbreth@gmail.com
    http://github.com/mattc58/fleetdb-python 
#####################################################################
 
This work is distributed under an MIT License: 
http://www.opensource.org/licenses/mit-license.php
 
The MIT License
 
Copyright (c) 2010 Matt Culbreth (http://mattculbreth.com)
 
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
 
The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.
 
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
 
#####################################################################
 
Unit tests for fleetdb-python
"""
import unittest
import uuid
import fleetdb

class TestClient(unittest.TestCase):
    '''
    Unit tests for the python-fleetdb library
    '''
    def setUp(self):
        '''
        set up the client
        '''
        self.client = fleetdb.FleetDBClient("localhost", 3400)
        
    def test_ping(self):
        '''
        test the ping method
        '''
        response = self.client.ping()
        self.assert_(response)
        
    def test_single_insert(self):
        '''
        test a single record insert
        '''
        response = self.client.insert("test", {'id' : uuid.uuid4().hex})
        self.assert_(response, 1)
        
    def test_multi_insert(self):
        '''
        test a multiple record insert
        '''
        response = self.client.insert("test", [{'id' : uuid.uuid4().hex}, {'id' : uuid.uuid4().hex}, {'id' : uuid.uuid4().hex}])
        self.assert_(response, 3)
        
    def test_insert_duplicate(self):
        '''
        test that an insert of a duplicate key throws an exception
        '''
        def test_insert_duplicates_inner():
            # first insert something
            id1 = uuid.uuid4().hex
            self.client.insert("test", {'id' : id1, 'name' : 'name1'})
        
            # now try the same key
            self.client.insert("test", {'id' : id1, 'name' : 'name2'})
            
        self.assertRaises(AssertionError, test_insert_duplicates_inner)
        
    def test_select(self):
        '''
        test a normal select
        '''
        # first insert something
        test_collection = uuid.uuid4().hex
        id1 = uuid.uuid4().hex
        self.client.insert(test_collection, {'id' : id1, 'name' : 'name1'})
        
        # now get it
        response = self.client.select(test_collection)
        self.assert_(response)
        self.assertEqual(1, len(response))
        
    def test_select_where(self):
        '''
        test a select with a where clause
        '''
        # first insert something
        test_collection = uuid.uuid4().hex
        id2 = uuid.uuid4().hex
        response = self.client.insert(test_collection, [{'id' : uuid.uuid4().hex}, {'id' : id2}, {'id' : uuid.uuid4().hex}])
        
        # get all 3
        response = self.client.select(test_collection)
        self.assert_(response)
        self.assertEqual(3, len(response))
        
        # now get 1
        response = self.client.select(test_collection, {'where' : ['=', 'id', id2]})
        self.assert_(response)
        self.assertEqual(1, len(response))


