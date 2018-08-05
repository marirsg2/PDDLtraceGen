begin_version
3
end_version
begin_metric
0
end_metric
6
begin_variable
var0
-1
3
Atom at(t3, l30)
Atom at(t3, l31)
Atom at(t3, l32)
end_variable
begin_variable
var1
-1
3
Atom at(t2, l20)
Atom at(t2, l21)
Atom at(t2, l22)
end_variable
begin_variable
var2
-1
3
Atom at(t1, l10)
Atom at(t1, l11)
Atom at(t1, l12)
end_variable
begin_variable
var3
-1
3
Atom at(t0, l00)
Atom at(t0, l01)
Atom at(t0, l02)
end_variable
begin_variable
var4
-1
4
Atom at(a0, l00)
Atom at(a0, l10)
Atom at(a0, l20)
Atom at(a0, l30)
end_variable
begin_variable
var5
-1
17
Atom at(p0, l00)
Atom at(p0, l01)
Atom at(p0, l02)
Atom at(p0, l10)
Atom at(p0, l11)
Atom at(p0, l12)
Atom at(p0, l20)
Atom at(p0, l21)
Atom at(p0, l22)
Atom at(p0, l30)
Atom at(p0, l31)
Atom at(p0, l32)
Atom in(p0, a0)
Atom in(p0, t0)
Atom in(p0, t1)
Atom in(p0, t2)
Atom in(p0, t3)
end_variable
0
begin_state
1
1
2
0
2
10
end_state
begin_goal
1
5 7
end_goal
68
begin_operator
drive-truck t0 l00 l01 c0
0
1
0 3 0 1
1
end_operator
begin_operator
drive-truck t0 l00 l02 c0
0
1
0 3 0 2
1
end_operator
begin_operator
drive-truck t0 l01 l00 c0
0
1
0 3 1 0
1
end_operator
begin_operator
drive-truck t0 l01 l02 c0
0
1
0 3 1 2
1
end_operator
begin_operator
drive-truck t0 l02 l00 c0
0
1
0 3 2 0
1
end_operator
begin_operator
drive-truck t0 l02 l01 c0
0
1
0 3 2 1
1
end_operator
begin_operator
drive-truck t1 l10 l11 c1
0
1
0 2 0 1
1
end_operator
begin_operator
drive-truck t1 l10 l12 c1
0
1
0 2 0 2
1
end_operator
begin_operator
drive-truck t1 l11 l10 c1
0
1
0 2 1 0
1
end_operator
begin_operator
drive-truck t1 l11 l12 c1
0
1
0 2 1 2
1
end_operator
begin_operator
drive-truck t1 l12 l10 c1
0
1
0 2 2 0
1
end_operator
begin_operator
drive-truck t1 l12 l11 c1
0
1
0 2 2 1
1
end_operator
begin_operator
drive-truck t2 l20 l21 c2
0
1
0 1 0 1
1
end_operator
begin_operator
drive-truck t2 l20 l22 c2
0
1
0 1 0 2
1
end_operator
begin_operator
drive-truck t2 l21 l20 c2
0
1
0 1 1 0
1
end_operator
begin_operator
drive-truck t2 l21 l22 c2
0
1
0 1 1 2
1
end_operator
begin_operator
drive-truck t2 l22 l20 c2
0
1
0 1 2 0
1
end_operator
begin_operator
drive-truck t2 l22 l21 c2
0
1
0 1 2 1
1
end_operator
begin_operator
drive-truck t3 l30 l31 c3
0
1
0 0 0 1
1
end_operator
begin_operator
drive-truck t3 l30 l32 c3
0
1
0 0 0 2
1
end_operator
begin_operator
drive-truck t3 l31 l30 c3
0
1
0 0 1 0
1
end_operator
begin_operator
drive-truck t3 l31 l32 c3
0
1
0 0 1 2
1
end_operator
begin_operator
drive-truck t3 l32 l30 c3
0
1
0 0 2 0
1
end_operator
begin_operator
drive-truck t3 l32 l31 c3
0
1
0 0 2 1
1
end_operator
begin_operator
fly-airplane a0 l00 l10
0
1
0 4 0 1
1
end_operator
begin_operator
fly-airplane a0 l00 l20
0
1
0 4 0 2
1
end_operator
begin_operator
fly-airplane a0 l00 l30
0
1
0 4 0 3
1
end_operator
begin_operator
fly-airplane a0 l10 l00
0
1
0 4 1 0
1
end_operator
begin_operator
fly-airplane a0 l10 l20
0
1
0 4 1 2
1
end_operator
begin_operator
fly-airplane a0 l10 l30
0
1
0 4 1 3
1
end_operator
begin_operator
fly-airplane a0 l20 l00
0
1
0 4 2 0
1
end_operator
begin_operator
fly-airplane a0 l20 l10
0
1
0 4 2 1
1
end_operator
begin_operator
fly-airplane a0 l20 l30
0
1
0 4 2 3
1
end_operator
begin_operator
fly-airplane a0 l30 l00
0
1
0 4 3 0
1
end_operator
begin_operator
fly-airplane a0 l30 l10
0
1
0 4 3 1
1
end_operator
begin_operator
fly-airplane a0 l30 l20
0
1
0 4 3 2
1
end_operator
begin_operator
load-airplane p0 a0 l00
1
4 0
1
0 5 0 12
1
end_operator
begin_operator
load-airplane p0 a0 l10
1
4 1
1
0 5 3 12
1
end_operator
begin_operator
load-airplane p0 a0 l20
1
4 2
1
0 5 6 12
1
end_operator
begin_operator
load-airplane p0 a0 l30
1
4 3
1
0 5 9 12
1
end_operator
begin_operator
load-truck p0 t0 l00
1
3 0
1
0 5 0 13
1
end_operator
begin_operator
load-truck p0 t0 l01
1
3 1
1
0 5 1 13
1
end_operator
begin_operator
load-truck p0 t0 l02
1
3 2
1
0 5 2 13
1
end_operator
begin_operator
load-truck p0 t1 l10
1
2 0
1
0 5 3 14
1
end_operator
begin_operator
load-truck p0 t1 l11
1
2 1
1
0 5 4 14
1
end_operator
begin_operator
load-truck p0 t1 l12
1
2 2
1
0 5 5 14
1
end_operator
begin_operator
load-truck p0 t2 l20
1
1 0
1
0 5 6 15
1
end_operator
begin_operator
load-truck p0 t2 l21
1
1 1
1
0 5 7 15
1
end_operator
begin_operator
load-truck p0 t2 l22
1
1 2
1
0 5 8 15
1
end_operator
begin_operator
load-truck p0 t3 l30
1
0 0
1
0 5 9 16
1
end_operator
begin_operator
load-truck p0 t3 l31
1
0 1
1
0 5 10 16
1
end_operator
begin_operator
load-truck p0 t3 l32
1
0 2
1
0 5 11 16
1
end_operator
begin_operator
unload-airplane p0 a0 l00
1
4 0
1
0 5 12 0
1
end_operator
begin_operator
unload-airplane p0 a0 l10
1
4 1
1
0 5 12 3
1
end_operator
begin_operator
unload-airplane p0 a0 l20
1
4 2
1
0 5 12 6
1
end_operator
begin_operator
unload-airplane p0 a0 l30
1
4 3
1
0 5 12 9
1
end_operator
begin_operator
unload-truck p0 t0 l00
1
3 0
1
0 5 13 0
1
end_operator
begin_operator
unload-truck p0 t0 l01
1
3 1
1
0 5 13 1
1
end_operator
begin_operator
unload-truck p0 t0 l02
1
3 2
1
0 5 13 2
1
end_operator
begin_operator
unload-truck p0 t1 l10
1
2 0
1
0 5 14 3
1
end_operator
begin_operator
unload-truck p0 t1 l11
1
2 1
1
0 5 14 4
1
end_operator
begin_operator
unload-truck p0 t1 l12
1
2 2
1
0 5 14 5
1
end_operator
begin_operator
unload-truck p0 t2 l20
1
1 0
1
0 5 15 6
1
end_operator
begin_operator
unload-truck p0 t2 l21
1
1 1
1
0 5 15 7
1
end_operator
begin_operator
unload-truck p0 t2 l22
1
1 2
1
0 5 15 8
1
end_operator
begin_operator
unload-truck p0 t3 l30
1
0 0
1
0 5 16 9
1
end_operator
begin_operator
unload-truck p0 t3 l31
1
0 1
1
0 5 16 10
1
end_operator
begin_operator
unload-truck p0 t3 l32
1
0 2
1
0 5 16 11
1
end_operator
0
