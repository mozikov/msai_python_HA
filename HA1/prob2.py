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

class Programmer(Employee):
    def __init__(self,
                name: str,
                dep_name: str,
                position: str,
                salary: int,
                career_history: List = None,
                main_language: str = None):
        super().__init__(name, dep_name, position, salary, career_history)
        self.main_languge = main_language

class Cleaner(Employee):
    def __init__(self,
                name: str,
                dep_name: str,
                position: str,
                salary: int,
                career_history: List = None,
                effectiveness: int = None):
        super().__init__(name, dep_name, position, salary, career_history)
        self.effectiveness = effectiveness

class Manager(Employee):
    def __init__(self,
                name: str,
                dep_name: str,
                position: str,
                salary: int,
                career_history: List = None,
                num_of_subordinates: int = None):
        super().__init__(name, dep_name, position, salary, career_history)
        self._num_of_subordinates = num_of_subordinates

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

class StuffUpdate:
    def __init__(self, cmpn: Company) -> None:
        Validate._class_validation(cmpn)
        self.cmpn = cmpn
    
    def hire(self, emp):
        Validate._class_validation(emp, target_cls=Employee)
        if Validate._hire_validation(self.cmpn, emp):
            self.cmpn.vacancies[emp.position] -= 1
            self.cmpn.departments[emp.dep_name] += emp
    
    def fire(self, emp):
        if Validate._fire_validation(self.cmpn, emp):
            self.cmpn.departments[emp.dep_name] -= emp

class Validate:
    @staticmethod
    def _class_validation(cls, target_cls=Company):
        if isinstance(cls, target_cls):
            return True
        else:
            raise TypeError(f'Class must be {target_cls} instance')
    
    @staticmethod
    def _hire_validation(cmpn, emp):
        if emp.dep_name in cmpn.departments.keys() and \
            cmpn.vacancies[emp.position] > 0:
            try:
                cmpn.vacancies[emp.position]
                return True
            except KeyError:
                print(f"Position {emp.position} is not from vaccancies")
        else:
            print("There is no such department in the company or no vacancies in it")
            return False
    
    @staticmethod
    def _fire_validation(cmpn, emp):
        all_stuff = [f.employees for f in cmpn.departments.values()]
        all_stuff = [item for sublist in all_stuff for item in sublist] 
        if emp in all_stuff:
            return True
        else:
            print(f'No employee {emp} in a companay {cmpn}')
            return False
        
emp1 = Programmer('Max', 'Big Things', 'worker', 10000, main_language='C#')
emp2 = Programmer('Maxim', 'Big Things', 'worker', 20000, main_language='Python')
emp3 = Manager('Ivan', 'Big Things', 'chiller', 30000, num_of_subordinates=10)
emp4 = Cleaner('Max1', 'Little Things', 'worker', 10001, effectiveness=100)
emp5 = Programmer('Maxim1', 'Little Things', 'worker', 20001)
emp6 = Programmer('Ivan1', 'Little Things', 'chiller', 30001)
emp7 = Manager('Ivan2', 'Little Things', 'worker', 30001)
vacancies1 = {"worker": 2, "chiller": 0}
vacancies2 = {"worker": 2, "cleaner": 2}
dep1 = Department('Big Things', "Vlad", [emp1, emp2, emp3])
dep2 = Department('Little Things', "Tim", [emp4, emp5, emp6])
broinc = Company({dep1.dep_name: dep1}, vacancies1)
brocorp = Company({dep2.dep_name: dep2}, vacancies2)
print(brocorp)
print(broinc)
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

print('\n\nNew tests')
broinc_management = StuffUpdate(broinc)

print('\nVacs before')
print(broinc.vacancies)
broinc_management.hire(emp7)

print('Vacs after')
print(broinc.vacancies)
print('\nDeps before dismissal')
print(broinc.departments.values())
broinc_management.fire(emp7)
print('\nDeps after dismissal')
print(broinc.departments.values())

# New tests

# Vacs before
# {'worker': 2, 'chiller': 0}
# Vacs after
# {'worker': 1, 'chiller': 0}

# Deps before dismissal
# dict_values([Dep: Big Things, head: Vlad (stuff of 3 employees),
# Dep: Little Things, head: Tim (stuff of 4 employees)])

# Deps after dismissal
# dict_values([Dep: Big Things, head: Vlad (stuff of 3 employees),
# Dep: Little Things, head: Tim (stuff of 3 employees)])
