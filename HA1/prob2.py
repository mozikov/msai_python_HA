from typing import List

class Employee():
    def __init__(self, name: str, dep_name: str, position: str, salary: int, career_history: List=None):
        self.name = name
        self.dep_name = dep_name
        self.position = position
        self.salary = salary
        self.career_history = career_history
    
    def __str__(self):
        return f"{self.name} from {self.department} dep, {self.position}"
    
class Department():
    def __init__(self, dep_name, head: str, employees: list):
        self.dep_name = dep_name
        self.head = head
        self.employees = employees

    def __str__(self):
        return f"Dep: {self.dep_name}, head: {self.head} (stuff of {len(self.employees)} employees)"

    def __repr__(self):
        return f"Dep: {self.dep_name}, head: {self.head} (stuff of {len(self.employees)} employees)"
    
    def __iadd__(self, other):
        if isinstance(other, Employee):
            self.employees.append(other)
            return self
        else:
            raise TypeError("You can add only Employee class")
    
    def __isub__(self, other):
        if isinstance(other, Employee):
            self.employees.remove(other)
            return self
        else:
            raise TypeError("You can fire only Employee class")
    

class Company():
    def __init__(self, departments: dict, vacancies: dict):
        self.departments = departments
        self.vacancies = vacancies

    def add_dep(self, dep):
        self.departments[dep.dep_name] = dep
    
    def hire(self, emp):
        if emp.dep_name in self.departments.keys():
            try:
                if self.vacancies[emp.position] > 0:
                    self.vacancies[emp.position] -= 1
                    self.departments[emp.dep_name] += emp
            except KeyError:
                print(f"Position {emp.position} is not from vaccancies")
        else:
            print("There is no such department in the company")
    
    def fire(self, emp):
        if emp.dep_name in self.departments.keys():
            try:
                self.departments[emp.dep_name] -= emp
            except Exception as err:
                print(err)
        else:
            print("There is no such department in the company")
    
    def intersection(self, other):
        return dict(set(self.vacancies.items()) & set(other.vacancies.items())) 

    def union(self, other):
        return dict(set(self.vacancies.items()) | set(other.vacancies.items()))     
    
    def __len__(self):
        return sum([len(f.employees) for f in self.departments.values()])

    def __lt__(self, other):
        return len(self) <  len(other)

    def __le__(self, other):
        return len(self) <=  len(other)

    def __gt__(self, other):
        return len(self) >  len(other)

    def __ge__(self, other):
        return len(self) >=  len(other)

    def __eq__(self, other):
        return len(self) ==  len(other)

    def __ne__(self, other):
        return len(self) != len(other)

    def __add__(self, other):
        return {k: self.vacancies.get(k, 0) + other.vacancies.get(k, 0) for k in set(self.vacancies) | set(other.vacancies)}

    def __sub__(self, other):
        return { k : other.vacancies[k] for k in set(other.vacancies) - set(self.vacancies) }


    def __repr__(self):
        body = '\n'.join([str(f) for f in self.departments])
        return "Company:\n" + body
    
emp1 = Employee('Max', 'Big Things', 'worker', 10000)
emp2 = Employee('Maxim', 'Big Things', 'worker', 20000)
emp3 = Employee('Ivan', 'Big Things', 'chiller', 30000)
emp4 = Employee('Max1', 'Little Things', 'worker', 10001)
emp5 = Employee('Maxim1', 'Little Things', 'worker', 20001)
emp6 = Employee('Ivan1', 'Little Things', 'chiller', 30001)
emp7 = Employee('Ivan2', 'Little Things', 'worker', 30001)

vacancies1 = {"worker": 2, "chiller": 0}
vacancies2 = {"worker": 2, "cleaner": 2}

dep1 = Department('Big Things', "Vlad", [emp1, emp2, emp3])
dep2 = Department('Little Things', "Tim", [emp4, emp5, emp6])

broinc = Company({dep1.dep_name: dep1}, vacancies1)

brocorp = Company({dep1.dep_name: dep2}, vacancies2)

print(broinc.union(brocorp))
print(broinc.intersection(brocorp))
print(broinc + brocorp)
print(broinc - brocorp)
print(broinc == broinc)
print(broinc.union(brocorp))
print(broinc)
broinc.add_dep(dep2)
print(broinc)
print(broinc.vacancies)
broinc.hire(emp7)
print(broinc.vacancies)
print(broinc.departments)
broinc.fire(emp7)
print(broinc.departments)
