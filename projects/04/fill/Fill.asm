// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed.
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.
@prevKeyPressed
M=0
// Put your code here.
(LOOP)
    @keyPressed
    M=0     // keyPressed = 0

    @KBD    // Key input register
    D=M     // set D to the value of the input key
    @SET_KEY_PRESSED_FLAG_ON
    D;JGT   // if D > 0 goto SET_KEY_PRESSED_FLAG_ON
(KEY_PRESSED_FLAG_RETURN)

    @prevKeyPressed
    D=M     // D=prevKeyPressed
    @keyPressed
    D=D-M   // D=prevKeyPressed - keyPressed

    @TOGGLE_SCREEN
    D;JNE   // if D != 0 goto TOGGLE_SCREEN
(TOGGLE_SCREEN_RETURN)

    @keyPressed
    D=M     // D=keyPressed
    @prevKeyPressed
    M=D     // prevKeyPressed = keyPressed

    @LOOP
    0;JMP   // goto LOOP

(SET_KEY_PRESSED_FLAG_ON)
    @keyPressed
    M=1     // keyPressed = 1

    @KEY_PRESSED_FLAG_RETURN
    0;JMP   // goto KEY_PRESSED_FLAG_RETURN

(TOGGLE_SCREEN)
    @SCREEN // Set the A register to point to the memory
            // word that is mapped to the 16 left-most
            // pixels of the top row of the screen.
    D=A
    @i      // i refers to some mem. location.
    M=D     // i=screen pointer start
(LOOP_SCREEN)
    @i
    D=M     // D=i
    @24576  // Last screen address => 24,576 = 16384 + 256 * 32
    D=A-D   // D=8192-i
    @TOGGLE_SCREEN_RETURN
    D;JLE   // if 8192-i <= 0 goto TOGGLE_SCREEN_RETURN

    @i
    A=M     // Set register A to value of i
    M=!M    // Toggle register pixels color at Memory[A]

    @i
    M=M+1 // i=i+1
    @LOOP_SCREEN
    0;JMP // goto LOOP_SCREEN

    @TOGGLE_SCREEN_RETURN
    0;JMP   // goto TOGGLE_SCREEN_RETURN
