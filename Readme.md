# RF Current Amplification Device Simulation

Author: Sean 

Main Affiliation: University of Seoul, Department of Electrical and Computer Engineering

Current Affiliation: North Carolina State University, Department of Electrical and Computer Engineering
Concentration: Power Semiconductor Device 
Software: SILVACO ATLAS, TonyPlot, Python  

## Project Overview

This repository contains SILVACO ATLAS simulation files for a novel RF current amplification device with SIT-like behavior.

The main purpose of this project is to investigate a semiconductor device structure that can provide high drain current, strong gate control, and useful current amplification characteristics for RF applications.

The device is designed and analyzed using SILVACO ATLAS. Python is used for post-processing, data extraction, plotting, and comparison between different simulation conditions.

## Research Motivation

Conventional MOSFET-like structures often show current saturation in the output curve due to channel pinch-off and carrier velocity saturation. However, for some RF and current amplification applications, a device with SIT-like behavior can be useful.

A Static Induction Transistor-like device can show a more resistive or linear Id-Vd behavior while still maintaining gate-controlled current modulation.

This project studies how structural parameters and contact work functions affect:

- Drain current
- Turn-on behavior
- Output curve linearity
- Transfer characteristics
- Transconductance
- Output conductance
- Current gain
- RF-related performance

## Device Concept

The simulated device is a vertical or quasi-vertical semiconductor structure with a wrapped oxide gate region.

The device contains:

- Schottky source contact
- MOS gate contact
- Ohmic drain contact
- Local n-type source mesa region
- Main n-type drift region
- Wrapped oxide gate structure
- Gate-controlled current path near the source-side mesa

The source contact uses a Schottky barrier to control carrier injection.  
The gate electrode modulates the potential barrier and electric field near the source-side channel region.  
The drain contact is treated as an Ohmic contact for carrier collection.

## Device Target

The target behavior of this device is:

- High drain current
- Early turn-on voltage
- Strong gate modulation
- SIT-like Id-Vd output curve
- Reduced current saturation
- High transconductance
- Useful current amplification for RF operation


Example condition:

```txt
Gate work function = 4.2 eV
Source work function = 4.8 eV
