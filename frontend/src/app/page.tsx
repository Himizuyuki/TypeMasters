'use client'
import { createContext, ReactElement, useEffect, useRef, useState } from "react"
import { TestComponent } from "./test"
import React from "react"

const dummyTexts = [
  "I am the fastest typer on the planet.",
  "Lebron James went straight to the NBA out of college.",
  "Pizza is high on fat and carbs."
]


export default function Home() {

  const [currentTypedWord, setCurrentTypedWord] = useState("")
  const [raceStarted, setRaceStarted] = useState(false)
  const inputRef = useRef<HTMLInputElement>(null)
  const [timeOfPrevInput, setTimeOfPrevInput] = useState(Date.now())
  const textToType = useRef("")
  const [correctWords, setCorrectWords] = useState("")
  const [[correctText, incorrectText, remainingText], setWordSplit] = useState(["", "", ""])

  function OnTextChange(event: React.ChangeEvent<HTMLInputElement>) {
    let currentTypedWord = event.target.value
    const currentTypedText = correctWords + currentTypedWord
    console.log(Date.now());
    console.log("time passed: ", Date.now() - timeOfPrevInput)
    setTimeOfPrevInput(Date.now())
    if (GetTextDivision(textToType.current, currentTypedText)[2].length == 0) { 
      alert("You won!")
    }
    setWordSplit(GetTextDivision(textToType.current, currentTypedText))
    if (currentTypedWord.charAt(currentTypedWord.length - 1) === " " && GetTextDivision(textToType.current,currentTypedText)[1].length === 0) {
      setCorrectWords(currentTypedText)
      currentTypedWord = ""
    }
    setCurrentTypedWord(currentTypedWord);
  }
  function StartRace() {
    textToType.current = GetRandomTextToType()
    setWordSplit(["","", textToType.current])
    setRaceStarted(true);
    setTimeOfPrevInput(Date.now())
    if (inputRef.current) {
      inputRef.current.focus();
    }
    else {
      console.error("Unable to focus on textInput")
    }
  }
  function GetRandomTextToType() {
    const idx = Math.floor(Math.random() * dummyTexts.length)
    return dummyTexts[idx]
  }


  function GetTextDivision(textToType: string, typedText: string): [string, string, string] {
    function GetSplittingIndices(textToType: string, typedText: string) {
      let idx1 = -1
      while (idx1 + 1 < Math.min(textToType.length, typedText.length) && textToType[idx1 + 1] === typedText[idx1 + 1]) {
        idx1++;
      }
      let idx2 = Math.min(textToType.length - 1, typedText.length - 1)
      return [idx1, idx2]
    }
    const [idx1, idx2] = GetSplittingIndices(textToType, typedText)
    return [textToType.slice(0, idx1 + 1), textToType.slice(idx1 + 1, idx2 + 1), textToType.slice(idx2 + 1, textToType.length)]
  }
  return (
    <>
    <input
      ref={inputRef}
      id="textbox"
      value={currentTypedWord}
      onChange={OnTextChange}
      readOnly={!raceStarted}
    />
    <div> Text to type: <span style={{ color: "blue" }}>{correctText}</span><span style={{ backgroundColor: "red" }}>{incorrectText}</span><span style={{ color: "black" }}>{remainingText}</span></div>
    <button onClick={StartRace}> click to start race</button >
    <div> <span>test</span><span>hello</span></div>

    
  </>
  )
}

