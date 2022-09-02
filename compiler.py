import ast
import utils
from ast import *
from utils import *
from x86_ast import *
import os
from typing import List, Tuple, Set, Dict

Binding = Tuple[Name, expr]
Temporaries = List[Binding]


class Compiler:

    ############################################################################
    # Remove Complex Operands
    ############################################################################

    def is_atm(self, atm):
        match atm:
            case Constant(i):
                return True
            case Name(v):
                return True
            case _:
                return isinstance(atm, str)

    def rco_exp(self, e: expr, need_atomic: bool) -> Tuple[expr, Temporaries]:
        # print("calling exp")
        if not need_atomic:
            return [e, []]
        else:
            match e:
                case Call(Name('input_int'), []):
                    return [Call(Name('input_int'), []), []]
                case UnaryOp(unartop, atm):
                    if self.is_atm(atm):
                        return [UnaryOp(unartop, atm), []]
                    else:
                        (re_exp, tmps) = self.rco_exp(atm, True)
                        temps = []
                        temps.extend(tmps)
                        temps.append(Name(utils.generate_name("temp")), temps)
                        return [UnaryOp(unartop), temps]
                case BinOp(left, binaryop, right):
                    temps = []
                    left_exp = left
                    right_exp = right
                    if not self.is_atm(left):
                        (left_exp, left_temps) = self.rco_exp(left, True)
                        temps.extend(left_temps)
                        left_name = utils.generate_name("temp")
                        temps.append((Name(left_name), left_exp))
                        left_exp = Name(left_name)

                    if not self.is_atm(right):
                        (right_exp, right_temps) = self.rco_exp(right, True)
                        temps.extend(right_temps)
                        right_name = utils.generate_name("temp")
                        temps.append((Name(right_name), right_exp))
                        right_exp = Name(right_name)
                    return [BinOp(left_exp, binaryop, right_exp), temps]

    pass

    def rco_stmt(self, s: stmt) -> List[stmt]:
        res = []
        match s:
            case Expr(Call(Name('print'), [atm])):
                for at in [atm]:
                    if self.is_atm(atm):
                        (exp_atm, temps) = self.rco_exp(at, False)
                        res.append(Expr(Call(Name('print'), [exp_atm])))
                    else:
                        (exp_atm, temps) = self.rco_exp(at, True)
                        for tmp in temps:
                            res.append(Assign([tmp[0]], tmp[1]))
                        exp = Expr(Call(Name('print'), [exp_atm]))
                        res.append(exp)
                return res

            case Expr(exp):
                if self.is_atm(exp):
                    (exp_atm, temps) = self.rco_exp(exp, False)
                    res.append(Expr(exp_atm))
                else:
                    (exp_atm, temps) = self.rco_exp(exp, True)
                    for tmp in temps:
                        res.append(Assign([tmp[0]], tmp[1]))
                res.append(Expr(exp_atm))
                return res

            case Assign([Name(var)], exp):
                if self.is_atm(exp):
                    (exp_atm, temps) = self.rco_exp(exp, False)
                    res.append(Assign([Name(var)], exp_atm))
                else:
                    (exp_atm, temps) = self.rco_exp(exp, True)
                    for tmp in temps:
                        res.append(Assign([tmp[0]], tmp[1]))
                    res.append(Assign([Name(var)], exp_atm))
                return res
            case _:
                print("Unknown type")
        pass

    def remove_complex_operands(self, p: Module) -> Module:
        match p:
            case Module(stmt):
                st_list = []
                for st in stmt:
                    re_list = self.rco_stmt(st)
                    st_list.extend(re_list)
                return Module(st_list)
            case _:
                print("Unknown type")

        pass

    ############################################################################
    # Select Instructions
    ############################################################################

    def select_arg(self, e: expr) -> arg:
        # YOUR CODE HERE
        pass

    def select_stmt(self, s: stmt) -> List[instr]:
        # YOUR CODE HERE
        pass

        # def select_instructions(self, p: Module) -> X86Program:

    #     # YOUR CODE HERE
    #     pass

    ############################################################################
    # Assign Homes
    ############################################################################

    def assign_homes_arg(self, a: arg, home: Dict[Variable, arg]) -> arg:
        # YOUR CODE HERE
        pass

    def assign_homes_instr(self, i: instr,
                           home: Dict[location, arg]) -> instr:
        # YOUR CODE HERE
        pass

    def assign_homes_instrs(self, ss: List[instr],
                            home: Dict[location, arg]) -> List[instr]:
        # YOUR CODE HERE
        pass

        # def assign_homes(self, p: X86Program) -> X86Program:

    #     # YOUR CODE HERE
    #     pass

    ############################################################################
    # Patch Instructions
    ############################################################################

    def patch_instr(self, i: instr) -> List[instr]:
        # YOUR CODE HERE
        pass

    def patch_instrs(self, ss: List[instr]) -> List[instr]:
        # YOUR CODE HERE
        pass

        # def patch_instructions(self, p: X86Program) -> X86Program:
    #     # YOUR CODE HERE
    #     pass

    ############################################################################
    # Prelude & Conclusion
    ############################################################################

    # def prelude_and_conclusion(self, p: X86Program) -> X86Program:
    #     # YOUR CODE HERE
    #     pass
