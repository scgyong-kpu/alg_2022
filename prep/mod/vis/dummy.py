class Dummy:
  def __getattr__(self, name):
    return self.dummy
  def dummy(self):
    pass
