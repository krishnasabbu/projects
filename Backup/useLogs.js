import { useContext } from 'react'
import LogsContext from 'app/contexts/LogsContext'

const useLogs = () => useContext(LogsContext);

export default useLogs;