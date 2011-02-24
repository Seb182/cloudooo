##############################################################################
#
# Copyright (c) 2009-2010 Nexedi SA and Contributors. All Rights Reserved.
#                    Gabriel M. Monnerat <gabriel@tiolive.com>
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsibility of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# guarantees and support are strongly adviced to contract a Free Software
# Service Company
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
##############################################################################

from cloudooo.handler.tests.handlerTestCase import HandlerTestCase, make_suite
from xmlrpclib import ServerProxy
from os.path import join
from base64 import encodestring, decodestring
from magic import Magic

DAEMON = True


class TestServer(HandlerTestCase):
  """Test XmlRpc Server. Needs cloudooo server started"""

  def afterSetUp(self):
    """Creates a connection with cloudooo server"""
    self.proxy = ServerProxy("http://%s:%s/RPC2" % \
        (self.hostname, self.cloudooo_port), allow_none=True)

  def testConvertPDFtoTxt(self):
    """Converts pdf to txt"""
    data = open(join('data', 'test.pdf'), 'r').read()
    document = self.proxy.convertFile(encodestring(data),
                                      "pdf",
                                      "txt")
    mime = Magic(mime=True)
    mimetype = mime.from_buffer(decodestring(document))
    self.assertEquals(mimetype, "text/plain")
  
  def testGetMetadataFromPdf(self):
    """test if metadata are extracted correctly"""
    data = open(join('data', 'test.pdf'), 'r').read()
    metadata = self.proxy.getFileMetadataItemList(encodestring(data), "pdf")
    self.assertEquals(metadata["title"],
                      'Free Cloud Alliance Presentation')

  def testSetMetadata(self):
    """Test if metadata is inserted correctly in document"""
    data = open(join('data', 'test.pdf'), 'r').read()
    new_data = self.proxy.updateFileMetadata(encodestring(data),
                                             "pdf",
                                             {"producer": "Cloudooo"})
    metadata = self.proxy.getFileMetadataItemList(new_data, "pdf")
    self.assertEquals(metadata["title"],
                      'Free Cloud Alliance Presentation')
    self.assertEquals(metadata["producer"], 'Cloudooo')


def test_suite():
  return make_suite(TestServer)