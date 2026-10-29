import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from scipy.integrate import solve_ivp

OUT = Path(__file__).resolve().parent / 'files'
OUT.mkdir(exist_ok=True)
g = 9.81
v0 = 25.0
alpha = np.deg2rad(6.0)
m = 0.145
rho = 1.225
Cd = 0.47
r = 0.0366
A = np.pi * r**2
k = 0.5 * rho * Cd * A
T0 = 2*v0*np.sin(alpha)/g
R0 = v0**2*np.sin(2*alpha)/g
H0 = (v0*np.sin(alpha))**2/(2*g)

def rhs(t, q):
    x,y,vx,vy = q
    v = np.hypot(vx,vy)
    return [vx,vy,-(k/m)*v*vx,-g-(k/m)*v*vy]

def ground(t,q):
    return q[1] if t > 1e-10 else 1e-10
ground.terminal=True
ground.direction=-1
q0 = [0,0,v0*np.cos(alpha),v0*np.sin(alpha)]
sol = solve_ivp(rhs, (0, 5), q0, events=ground, dense_output=True, rtol=1e-10, atol=1e-12, max_step=0.002)
assert sol.status == 1, sol.message
Td = sol.t_events[0][0]
t = np.linspace(0, max(T0,Td), 1500)
t0 = t[t<=T0]
td = t[t<=Td]
x0=v0*np.cos(alpha)*t0
y0=v0*np.sin(alpha)*t0-.5*g*t0**2
vx0=np.full_like(t0,v0*np.cos(alpha)); vy0=v0*np.sin(alpha)-g*t0
xd,yd,vxd,vyd=sol.sol(td)
rd=sol.sol(Td)[0]
hd=np.max(yd)
Ed0=.5*m*v0**2
E0=.5*m*(vx0**2+vy0**2)+m*g*y0
Ed=.5*m*(vxd**2+vyd**2)+m*g*yd

def finish(filename):
    plt.grid(alpha=.3); plt.tight_layout(); plt.savefig(OUT/filename,dpi=175); plt.close()

plt.figure(figsize=(9,4.8));plt.plot(x0,y0,label='Bez oporu');plt.plot(xd,yd,label='Z oporem');plt.xlabel('Położenie x [m]');plt.ylabel('Wysokość y [m]');plt.title('Tor rzutu ukośnego');plt.legend();finish('tor.png')
plt.figure(figsize=(9,4.8));plt.plot(t0,x0,label='x(t), bez oporu');plt.plot(td,xd,'--',label='x(t), z oporem');plt.plot(t0,y0,label='y(t), bez oporu');plt.plot(td,yd,'--',label='y(t), z oporem');plt.xlabel('Czas t [s]');plt.ylabel('Położenie [m]');plt.title('Współrzędne w funkcji czasu');plt.legend();finish('polozenie.png')
plt.figure(figsize=(9,4.8));plt.plot(t0,vx0,label='vx, bez oporu');plt.plot(td,vxd,'--',label='vx, z oporem');plt.plot(t0,vy0,label='vy, bez oporu');plt.plot(td,vyd,'--',label='vy, z oporem');plt.xlabel('Czas t [s]');plt.ylabel('Prędkość [m/s]');plt.title('Składowe prędkości');plt.legend();finish('predkosc.png')
plt.figure(figsize=(9,4.8));plt.plot(t0,np.hypot(vx0,vy0),label='Bez oporu');plt.plot(td,np.hypot(vxd,vyd),label='Z oporem');plt.xlabel('Czas t [s]');plt.ylabel('Szybkość [m/s]');plt.title('Wartość prędkości');plt.legend();finish('szybkosc.png')
plt.figure(figsize=(9,4.8));plt.plot(t0,E0,label='Bez oporu');plt.plot(td,Ed,label='Z oporem');plt.xlabel('Czas t [s]');plt.ylabel('Energia mechaniczna [J]');plt.title('Bilans energii mechanicznej');plt.legend();finish('energia.png')
plt.figure(figsize=(9,4.8));plt.plot(t0,-g*np.ones_like(t0),label='ay, bez oporu');plt.plot(td,[-g-(k/m)*np.hypot(vxd[i],vyd[i])*vyd[i] for i in range(len(td))],label='ay, z oporem');plt.plot(td,-(k/m)*np.hypot(vxd,vyd)*vxd,label='ax, z oporem');plt.xlabel('Czas t [s]');plt.ylabel('Przyspieszenie [m/s²]');plt.title('Składowe przyspieszenia');plt.legend();finish('przyspieszenie.png')
print(f'Bez oporu: T={T0:.6f} s, R={R0:.6f} m, H={H0:.6f} m')
print(f'Z oporem:  T={Td:.6f} s, R={rd:.6f} m, H={hd:.6f} m')
print(f'k={k:.10f} kg/m; E0={Ed0:.6f} J; E_koniec={Ed[-1]:.6f} J')
