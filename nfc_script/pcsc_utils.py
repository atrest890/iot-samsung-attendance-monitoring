#!/usr/bin/env python3

from smartcard.scard import ( SCARD_S_SUCCESS, 
                              SCARD_STATE_ATRMATCH,
                              SCARD_STATE_UNAWARE, 
                              SCARD_STATE_UNAVAILABLE, 
                              SCARD_STATE_IGNORE, 
                              SCARD_STATE_EMPTY, 
                              SCARD_STATE_PRESENT, 
                              SCARD_STATE_EXCLUSIVE,
                              SCARD_STATE_INUSE,
                              SCARD_STATE_MUTE,
                              SCARD_STATE_CHANGED,
                              SCARD_STATE_UNKNOWN,
                              SCardGetErrorMessage
                             )
import smartcard.util

DEBUG_PRINT = False

def check(hresult, op_des, printManualy = -1):
    if hresult != SCARD_S_SUCCESS:
        raise Exception('Failed to {0}: {1}\nhresult = {2}'.format(op_des, SCardGetErrorMessage(hresult), hresult))
    elif (DEBUG_PRINT and type(printManualy) == int) or printManualy:
        print('Success to ' + op_des)

def printState(state):
    reader, eventstate, atr = state
    print(reader + " " + smartcard.util.toHexString(atr, smartcard.util.HEX))
    if eventstate & SCARD_STATE_ATRMATCH:
        print('\tCard found')
    if eventstate & SCARD_STATE_UNAWARE:
        print('\tState unaware')
    if eventstate & SCARD_STATE_IGNORE:
        print('\tIgnore reader')
    if eventstate & SCARD_STATE_UNAVAILABLE:
        print('\tReader unavailable')
    if eventstate & SCARD_STATE_EMPTY:
        print('\tReader empty')
    if eventstate & SCARD_STATE_PRESENT:
        print('\tCard present in reader')
    if eventstate & SCARD_STATE_EXCLUSIVE:
        print('\tCard allocated for exclusive use by another application')
    if eventstate & SCARD_STATE_INUSE:
        print('\tCard in used by another application but can be shared')
    if eventstate & SCARD_STATE_MUTE:
        print('\tCard is mute')
    if eventstate & SCARD_STATE_CHANGED:
        print('\tState changed')
    if eventstate & SCARD_STATE_UNKNOWN:
        print('\tState unknowned')

def insertedCardState(state):
    _, eventstate, _ = state
    return eventstate & SCARD_STATE_ATRMATCH

def printResponse(resp, text):
    print(text, smartcard.util.toHexString(resp, smartcard.util.HEX))

# def waitToChange():