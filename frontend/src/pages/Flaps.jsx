import { useEffect, useState } from "react"
import api from "../api/api"
import { Card, Progress, Table, DatePicker } from "antd"
import { ApiOutlined } from "@ant-design/icons"
import { red, green } from '@ant-design/colors';
import { AiFillCaretUp, AiFillCaretDown } from 'react-icons/ai'
const { Meta } = Card;
import dayjs from 'dayjs';

const { RangePicker } = DatePicker;

function Flaps() {
  const [data, setData] = useState([])
  const [progress, setProgress] = useState('');
  const [loading, setLoading] = useState(true);
  const [counter, setCounter] = useState(10); // Initial counter value in seconds
  const [initDate, setInitDate] = useState(new Date().setHours(0, 0, 0, 0))
  const [endDate, setEndDate] = useState(999999999999999)

  async function fetchData() {
    try {
      const response = await api.get('/if_status', {
        onDownloadProgress: (e) => {
          const progress = Math.round((e.loaded * 100) / e.total);
          setProgress(progress);
        }
      });
      setData(response.data);
      setLoading(false);
    } catch (error) {
      console.log(error);
    }
  }

  useEffect(() => {
    fetchData(); // Initial data fetch
    const interval = setInterval(() => {
      fetchData(); // Fetch data every 10 seconds
      setCounter(10); // Reset the counter
    }, 10000); // 10000 milliseconds = 10 seconds

    return () => {
      clearInterval(interval); // Clean up the interval when the component unmounts
    };
  }, []);

  useEffect(() => {
    // Update the counter every second
    const counterInterval = setInterval(() => {
      setCounter((prevCounter) => prevCounter - 1);
    }, 1000);

    return () => {
      clearInterval(counterInterval); // Clean up the counter interval
    };
  }, []);

  function convertData(date) {
    const dataconverted = new Date(date).getTime()
    return dataconverted
  }

  function convertData2(date) {
    // Create a Date object from the input date string
    const dateObject = new Date(date);

    // Convert the date to GMT-3
    dateObject.setHours(dateObject.getHours() - 3);

    // Get the timestamp of the resulting date
    const timestampInGMTMinus3 = dateObject.getTime();

    return timestampInGMTMinus3;
  }

  function convertGMT(date) {
    return `${new Date(date).toLocaleDateString()} - ${new Date(date).getUTCHours()}:${new Date(date).getMinutes() < 10 ? `0${new Date(date).getMinutes()}` : new Date(date).getMinutes()}`
  }

  function getUniqueIPs(arr) {
    const uniqueIPs = new Set();
    const result = [];

    for (const item of arr) {
        if (!uniqueIPs.has(item.ip)) {
            uniqueIPs.add(item.ip);
            result.push({ text: item.ip, value: item.ip });
        }
    }

    return result;

}


console.log(getUniqueIPs(data))


  const columns = [
    {
      "title": "#",
      "key": "id",
      "dataIndex": "id",
      defaultSortOrder: 'descend',
      sorter: (a, b) => a.id - b.id,
    },
    {
      "title": "IP",
      "key": "ip",
      "dataIndex": "ip",
      render: (ip) => <a href={`telnet://${ip}`}>{ip} <ApiOutlined /></a>,
      onFilter: (value, record) => record.ip.startsWith(value),
      filterSearch: true,
      filters: 
        getUniqueIPs(data)
      ,

    },
    {
      "title": "Horário",
      "key": "horario",
      "dataIndex": "horario",
      render: (text) => <p>{convertGMT(text)}</p>
    },
    {
      "title": "Interface",
      "key": "interface",
      "dataIndex": "interface"
    },
    {
      "title": "Admin Status",
      "key": "admin_status",
      "dataIndex": "admin_status",
      render: (text) => <p>{text.physical_status === "down" ? <AiFillCaretDown style={{ color: 'red' }} /> : <AiFillCaretUp style={{ color: "green" }} />}</p>
    },
    {
      "title": "Status Físico",
      "key": "physical_status",
      render: (text) => <p>{text.physical_status === "down" ? <AiFillCaretDown style={{ color: 'red' }} /> : <AiFillCaretUp style={{ color: "green" }} />}</p>
    },
    {
      "title": "Descrição",
      "key": "descricao",
      "dataIndex": "descricao",
      filters: [
        {
          text: 'Backbone',
          value: 'BB-',
        },
        {
          text: 'PMS',
          value: 'PMS',
        },
        {
          text: 'Trânsito',
          value: 'transit',
        },
      ],
      onFilter: (value, record) => record.descricao.startsWith(value),
      filterSearch: true,
      render: (text) => <p>{text != "" ? text : "NO DESCRIPTION"}</p>
    }
  ]

  const filteredData = data.filter(item => {
    const horario = convertData(item.horario);
    return horario >= initDate && horario <= endDate;
  });


  return (
    <Card
      extra={<Progress percent={progress} steps={5} size="small" strokeColor={green[6]} />}
      title={<div>Filtrar: <RangePicker
        size="small"
        bordered={false}
        showTime
        format="DD-MM-YYYY HH:mm:ss"
        onChange={(e) => {
          if (e) { setInitDate(convertData2(e[0].$d)), setEndDate(convertData2(e[1].$d)) } else { setInitDate(0), setEndDate(9999999999999) }

        }}
      />
      </div>}
    >
      <Table dataSource={filteredData} columns={columns} loading={loading} />
    </Card>
  )
}

export default Flaps
