import copy
import unittest
from update import render

class ManifestValidation(unittest.TestCase):
    def setUp(self):
        self.manifest = {'version':'1.2.3','tag':'personal-v1.2.3','commit':'a'*40,'repository':'sasha00123/zed','cask':'zed-custom','app_name':'Zed Custom','bundle_id':'io.sasha00123.ZedCustom','source_asset':'zed-custom-1.2.3-source.tar.gz','assets':[
            {'architecture':arch,'asset':f'zed-custom-1.2.3-macos-{arch}.zip','sha256':'b'*64} for arch in ('arm64',)]}
        self.release = {'draft':False,'prerelease':False,'tag_name':'personal-v1.2.3','assets':[
            {'name':a['asset'],'digest':'sha256:'+a['sha256']} for a in self.manifest['assets']]+[{'name':self.manifest['source_asset']}]}
    def test_valid_cask(self):
        text=render('zed',self.release,self.manifest)
        self.assertIn('cask "zed-custom"',text)
        self.assertIn('depends_on arch: :arm64',text)
        self.assertIn('-macos-arm64.zip',text)
        self.assertNotIn('intel:',text)
        self.assertIn('depends_on formula: "git"',text)
    def test_rejects_upstream_identity(self):
        self.manifest['bundle_id']='dev.zed.Zed'
        with self.assertRaises(ValueError):render('zed',self.release,self.manifest)
    def test_rejects_draft(self):
        self.release['draft']=True
        with self.assertRaises(ValueError):render('zed',self.release,self.manifest)
    def test_rejects_digest_mismatch(self):
        self.release['assets'][0]['digest']='sha256:'+'c'*64
        with self.assertRaises(ValueError):render('zed',self.release,self.manifest)
    def test_rejects_missing_source(self):
        self.release['assets'].pop()
        with self.assertRaises(ValueError):render('zed',self.release,self.manifest)
    def test_rejects_missing_architecture(self):
        self.manifest['assets'].pop()
        with self.assertRaises(ValueError):render('zed',self.release,self.manifest)
    def test_rejects_intel_asset(self):
        self.manifest['assets'][0]['architecture']='x86_64'
        with self.assertRaises(ValueError):render('zed',self.release,self.manifest)
    def test_rejects_injected_version(self):
        self.manifest['version']='1.2.3"; system("no")'
        with self.assertRaises(ValueError):render('zed',self.release,self.manifest)

if __name__=='__main__':unittest.main()
