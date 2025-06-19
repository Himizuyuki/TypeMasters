'use client'
import { ChangeEventHandler, useEffect, useRef, useState } from "react"

const dummyTexts = [
  "I am the fastest typer on the planet.",
  "Lebron James went straight to the NBA out of college.",
  "Pizza is high on fat and carbs."
]

export default function Home() {
  const [textValue, setTextValue] = useState("")
  const [raceStarted, setRaceStarted] = useState(false)
  const inputRef = useRef<HTMLInputElement>(null)
  const [timeOfPrevInput, setTimeOfPrevInput] = useState(Date.now())
  const [textToType, setTextToType] = useState("")


  function OnTextChange(event: React.ChangeEvent<HTMLInputElement>) {
    setTextValue(event.target.value);
    console.log(Date.now());
    console.log("time passed: ", Date.now() - timeOfPrevInput)
    setTimeOfPrevInput(Date.now())
  }

  function StartRace() {
    setTextToType(GetRandomTextToType())
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

  return (
    <>
      <input
        ref={inputRef}
        id="textbox"
        value={textValue}
        onChange={OnTextChange}
        readOnly={!raceStarted}
      />
      <div> Here is the value {textValue} </div>
      <button onClick={StartRace}> click to start race </button >
      <div> Text to type: {textToType} </div>
    </>
  )
}
