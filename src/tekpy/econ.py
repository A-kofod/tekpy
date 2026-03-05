import math
import sympy as sp


class TotalMetoden:
    """Retunerer optimal afsætning og tilhørende pris, given pris/afs function og VE
    DB_total kan regnes ved .DB_tot()"""
    def __init__(self, a, b, VE):
        self.a = a
        self.b = b
        self.VE = VE
        self.x = sp.symbols('x')
    
    def DB_x(self):
        DB = (self.a * self.x + self.b) * self.x - self.VE * self.x
        DB_dif = sp.diff(DB, self.x)
        afs_opt = sp.solve(DB_dif, self.x)[0]
        self.afs_opt = afs_opt
        return self.afs_opt
    
    def px(self):
        p = self.a * self.x + self.b
        self.p_opt = p.subs(self.x, self.afs_opt)
        return self.p_opt
    
    def DB_tot(self):
        self.db_tot = self.afs_opt * self.p_opt - self.VE * self.afs_opt
        return self.db_tot
    
class DifferensMetoden:
    """Retunerer afs_opt, pris_opt hvis DOMK er givet"""
    def __init__(self, DOMK, a, b) -> float:
        self.DOMK = DOMK
        self.a = a
        self.b = b
        self.x = sp.symbols('x')
        self.px = self.a * self.x + self.b
        self.oms = self.px * self.x

    def afs_opt(self) -> float:
        DOMS = sp.diff(self.px * self.x, self.x)
        self.afs = sp.solve(sp.Eq(DOMS, self.DOMK), self.x)[0]
        return self.afs
    
    def pris_opt(self):
        p_opt = self.px.subs(self.x, self.afs_opt())
        return p_opt

