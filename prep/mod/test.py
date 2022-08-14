import vis

p = vis.Animal()
c = vis.Dog()

print(c.value)

d = vis.Dummy()
print(d.hello)
print(d.world())

# polymorphism
d1 = vis.Dog()
d2 = vis.Jindogae()
dogs = [d1, d2]
for dog in dogs:
  print(dog.bark())
