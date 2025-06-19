'use client'
import { ChangeEventHandler, useRef, useState } from "react"


export default function Home() {



  const [textValue, setTextValue] = useState("")
  const [raceStarted, setRaceStarted] = useState(false)
  const inputRef = useRef<HTMLInputElement>(null)
  const [timeOfPrevInput, setTimeOfPrevInput] = useState(Date.now())


  function OnTextChange(event: React.ChangeEvent<HTMLInputElement>) {
    setTextValue(event.target.value);
    console.log(Date.now());
    console.log("time passed: ", Date.now() - timeOfPrevInput)
    setTimeOfPrevInput(Date.now())
  }

  function StartRace() {
    setRaceStarted(true);
    setTimeOfPrevInput(Date.now())
    if (inputRef.current) {
      inputRef.current.focus();
    }
    else {
      console.error("Unable to focus on textInput")
    }
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
    </>
  )
}
