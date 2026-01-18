import React, { useState } from "react"
import style from './App.module.scss'

type ArticleContent = {
    article_id: number,
    id: number,
    content: string
}

type Article = {
    id: number,
    title: string,
    author: string,
    link: string,
    published_date: string,
    pdf_path: string,
    content: ArticleContent
}


type BackendDataResponse = Article[]

type DateType = {
    day: number,
    month: number,
    year: number
}

const API_URL =
    import.meta.env.VITE_API_URL || "http://localhost:8000"

const App: React.FC = () => {
    const [data, setData] = useState<BackendDataResponse | null>(null)
    const [loading, setLoading] = useState<boolean>(true)
    const [error, setError] = useState<string | null>(null)

    const [startDate, setStartDate] = useState<DateType>(
        {
            day: 10,
            month: 10,
            year: 2025
        }
    )
    const [endDate, setEndDate] = useState<DateType>(
        {
            day: 20,
            month: 10,
            year: 2025
        }
    )

    const [inputData, setInputData] = useState<string>("")

    const [openArticleId, setOpenArticleId] = useState<number | null>(null)

    const minYear = 1900
    const maxYear = 2100

    const toggleArticle = (id: number) => {
        setOpenArticleId(prev => (prev === id ? null : id))
    }

    const getDaysInMonth = (year: number, month: number) => new Date(year, month, 0).getDate()


    const incrementDay = (setDate: React.Dispatch<React.SetStateAction<DateType>>) => {
        setDate(prev => {
            const maxDay = getDaysInMonth(prev.year, prev.month)
            if (prev.day >= maxDay) return prev
            return { ...prev, day: prev.day + 1 }
        })
    }

    const decrementDay = (setDate: React.Dispatch<React.SetStateAction<DateType>>) => {
        setDate(prev => {
            if (prev.day <= 1) return prev
            return { ...prev, day: prev.day - 1 }
        })
    }

    const incrementMonth = (setDate: React.Dispatch<React.SetStateAction<DateType>>) => {
        setDate(prev => {
            if (prev.month >= 12) return prev

            const newMonth = prev.month + 1
            const maxDay = getDaysInMonth(prev.year, newMonth)

            return {
                ...prev,
                month: newMonth,
                day: Math.min(prev.day, maxDay),
            }
        })
    }

    const decrementMonth = (setDate: React.Dispatch<React.SetStateAction<DateType>>) => {
        setDate(prev => {
            if (prev.month <= 1) return prev

            const newMonth = prev.month - 1
            const maxDay = getDaysInMonth(prev.year, newMonth)

            return {
                ...prev,
                month: newMonth,
                day: Math.min(prev.day, maxDay),
            }
        })
    }

    const incrementYear = (setDate: React.Dispatch<React.SetStateAction<DateType>>) => {
        setDate(prev => {
            if (prev.year >= maxYear) return prev

            const newYear = prev.year + 1
            const maxDay = getDaysInMonth(newYear, prev.month)

            return {
                ...prev,
                year: newYear,
                day: Math.min(prev.day, maxDay),
            }
        })
    }

    const decrementYear = (setDate: React.Dispatch<React.SetStateAction<DateType>>) => {
        setDate(prev => {
            if (prev.year <= minYear) return prev

            const newYear = prev.year - 1
            const maxDay = getDaysInMonth(newYear, prev.month)

            return {
                ...prev,
                year: newYear,
                day: Math.min(prev.day, maxDay),
            }
        })
    }



    const fetchHello = async () => {
        try {
            const res = await fetch(`${API_URL}/article?word=${inputData}&start_date=${String(startDate.day).padStart(2, "0")}.${String(startDate.month).padStart(2, "0")}.${String(startDate.year)}&end_date=${String(endDate.day).padStart(2, "0")}.${String(endDate.month).padStart(2, "0")}.${String(endDate.year)}`)

            if (!res.ok) {
                throw new Error(`Request failed with status ${res.status}`)
            }

            const json: BackendDataResponse = await res.json()
            console.log(res)
            console.log(json)
            setData(json)
        } catch (err: unknown) {
            if (err instanceof Error) {
                setError(err.message)
                console.error(err)
            } else {
                setError("Unknown error")
                console.error(err)
            }
        } finally {
            setLoading(false)
        }
    }

    return (
        <div className={style.mainContainer}>
            <div className={style.inputData}>
                <div className={style.inputDataContainer}>
                    <h2>Scrapper for: <a>https://www.polityka.pl</a></h2>

                    <form className={style.inputDataTable}>
                        <div className={style.startDateContainer}>
                            <h2>Start Date</h2>
                            <div style={{ display: "flex", width: "100%" }}>
                                <div className={style.dateItem}>
                                    <button type='button' className={style.dateIncrementBtn} onClick={() => incrementDay(setStartDate)}>&#8593;</button>
                                    <div className={style.showDate}>
                                        <span>{String(startDate.day).padStart(2, "0")}</span>
                                    </div>
                                    <button type='button' className={style.dateDecrementBtn} onClick={() => decrementDay(setStartDate)}>&#8595;</button>
                                </div>

                                <div className={style.dateItem}>
                                    <button type='button' className={style.dateIncrementBtn} onClick={() => incrementMonth(setStartDate)}>&#8593;</button>
                                    <div className={style.showDate}>
                                        <span>{String(startDate.month).padStart(2, "0")}</span>
                                    </div>
                                    <button type='button' className={style.dateDecrementBtn} onClick={() => decrementMonth(setStartDate)}>&#8595;</button>
                                </div>

                                <div className={style.dateItem}>
                                    <button type='button' className={style.dateIncrementBtn} onClick={() => incrementYear(setStartDate)}>&#8593;</button>
                                    <div className={style.showDate}>
                                        <span>{startDate.year}</span>
                                    </div>
                                    <button type='button' className={style.dateDecrementBtn} onClick={() => decrementYear(setStartDate)}>&#8595;</button>
                                </div>
                            </div>
                        </div>
                        <div className={style.endDateContainer}>
                            <h2>End Date</h2>
                            <div style={{ display: "flex", width: "100%" }}>
                                <div className={style.dateItem}>
                                    <button type='button' className={style.dateIncrementBtn} onClick={() => incrementDay(setEndDate)}>&#8593;</button>
                                    <div className={style.showDate}>
                                        <span>{String(endDate.day).padStart(2, "0")}</span>
                                    </div>
                                    <button type='button' className={style.dateDecrementBtn} onClick={() => decrementDay(setEndDate)}>&#8595;</button>
                                </div>

                                <div className={style.dateItem}>
                                    <button type='button' className={style.dateIncrementBtn} onClick={() => incrementMonth(setEndDate)}>&#8593;</button>
                                    <div className={style.showDate}>
                                        <span>{String(endDate.month).padStart(2, "0")}</span>
                                    </div>
                                    <button type='button' className={style.dateDecrementBtn} onClick={() => decrementMonth(setEndDate)}>&#8595;</button>
                                </div>

                                <div className={style.dateItem}>
                                    <button type='button' className={style.dateIncrementBtn} onClick={() => incrementYear(setEndDate)}>&#8593;</button>
                                    <div className={style.showDate}>
                                        <span>{endDate.year}</span>
                                    </div>
                                    <button type='button' className={style.dateDecrementBtn} onClick={() => decrementYear(setEndDate)}>&#8595;</button>
                                </div>
                            </div>
                        </div>
                        <div className={style.inputWordContainer}>
                            <label htmlFor="wordInput">Please enter a word to search</label>
                            <input name="wordInput" type="text" value={inputData} onChange={(e) => setInputData(e.target.value)} />
                        </div>
                    </form>
                    <div className={style.submitBtnContainer}>
                        <button className={style.submitFormBtn}
                            onClick={fetchHello}
                        >Submit</button>
                    </div>
                </div>
            </div >
            <div className={style.showDataContainer}>
                {loading && <p className={style.info}>Loading...</p>}
                {error && <p className={style.error}>{error}</p>}

                {data && data.length > 0 && (
                    <table className={style.articlesTable}>
                        <thead>
                            <tr>
                                <th>#</th>
                                <th>Title</th>
                                <th>Author</th>
                                <th>Published</th>
                                <th>Link</th>
                            </tr>
                        </thead>
                        <tbody>
                            {data.map((article, index) => (
                                <React.Fragment key={article.id}>
                                    <tr
                                        className={style.tableRow}
                                        onClick={() => toggleArticle(article.id)}
                                    >
                                        <td>{index + 1}</td>
                                        <td className={style.titleCell}>{article.title}</td>
                                        <td>{article.author}</td>
                                        <td>{article.published_date}</td>
                                        <td>
                                            <button className={style.detailsBtn}>
                                                {openArticleId === article.id ? "Hide" : "Details"}
                                            </button>
                                        </td>
                                    </tr>

                                    {openArticleId === article.id && (
                                        <tr className={style.expandedRow}>
                                            <td colSpan={5}>
                                                <div className={style.expandedContent}>
                                                    <div className={style.pdfBlock}>
                                                        <strong>PDF:</strong>{" "}
                                                        <a
                                                            href={`${API_URL}/${article.pdf_path}`}
                                                            target="_blank"
                                                            rel="noopener noreferrer"
                                                        >
                                                            Open PDF
                                                        </a>
                                                    </div>

                                                    <div className={style.textBlock}>
                                                        <strong>Content:</strong>
                                                        <p>
                                                            {article.content.content || "No content"}
                                                        </p>
                                                    </div>
                                                </div>
                                            </td>
                                        </tr>
                                    )}
                                </React.Fragment>
                            ))}
                        </tbody>
                    </table>
                )}

                {data && data.length === 0 && (
                    <p className={style.info}>No articles found</p>
                )}
            </div>
        </div >
    )
}

export default App
