import React, { useState, useEffect } from 'react';
import { Button, Card, Collapse, Divider, List, Progress, Select, Table, notification, Row, Col } from 'antd';
import { Input } from 'antd';
import api from '../api/api';
const { Search } = Input;


const AntiGuerreiro = () => {
  const [asnSearch, setAsnSearch] = useState('');
  const [allAttackData, setAllAttackData] = useState([]);
  const [groupedAttacks, setGroupedAttacks] = useState({});
  const [loadingProgress, setLoadingProgress] = useState(0);
  const [dataLoaded, setDataLoaded] = useState(false);
  const [attackUpdates, setAttackUpdates] = useState({});
  const [prefixSearch, setPrefixSearch] = useState('');


  const handleSearchChange = () => {
    const filteredData = allAttackData.filter(attack =>
      attack.asn.toLowerCase().includes(asnSearch.toLowerCase()) &&
      attack.prefix.toLowerCase().includes(prefixSearch.toLowerCase())
    );
    setGroupedAttacks(groupAttacksByAsn(filteredData));
  };


  useEffect(() => {
    api.get('/api/attacks')
      .then(response => {
        const data = response.data.data;
        setAllAttackData(data);
        setGroupedAttacks(groupAttacksByAsn(data));
      })
      .catch(error => console.error('Error fetching data:', error));
  }, []);

  const handleAsnSearchChange = (searchQuery) => {
    // searchQuery is a string, not an event object
    setAsnSearch(searchQuery);
    const filteredData = allAttackData.filter(attack =>
      attack.asn.toLowerCase().includes(searchQuery.toLowerCase())
    );
    setGroupedAttacks(groupAttacksByAsn(filteredData));
  };

  const handleInputChange = (e) => {
    setAsnSearch(e.target.value);
  };

  useEffect(() => {
    // Simulate data loading and increment progress
    const loadData = () => {
      setLoadingProgress(prevProgress => {
        if (prevProgress < 100) {
          setTimeout(loadData, 100); // Adjust time for your data loading
          return prevProgress + 10; // Adjust increment value based on your data loading
        } else {
          setDataLoaded(true);
          return 100;
        }
      });
    };

    loadData();
    // Replace the above with your actual data fetching logic
    // and update the progress as the data is being fetched.
  }, []);

  const handleBandwidthChange = (value, key) => {
    // Atualize o estado com o novo valor de bandwidth
    setAttackUpdates(prevUpdates => ({
      ...prevUpdates,
      [key]: { ...prevUpdates[key], bandwidth: value }
    }));
  };

  const handleActionChange = (value, key) => {
    // Atualize o estado com o novo valor de action
    console.log(value)
    setAttackUpdates(prevUpdates => ({
      ...prevUpdates,
      [key]: { ...prevUpdates[key], action: value }
    }));
  };

  const handleUpdate = (asn, key) => {
    const update = attackUpdates[key];
    if (update) {
      api.post(`/api/attacks/${asn}`, update)
        .then(response => {
          notification.success({ message: response.data.data })
        })
        .catch(error => notification.error({ message: error }));
    } else {
      notification.error({ message: 'Nenhuma alteração foi feita.' })
    }
  }

  const groupAttacksByAsn = (attacks) => {
    return attacks.reduce((acc, attack) => {
      if (!acc[attack.asn]) {
        acc[attack.asn] = [];
      }
      acc[attack.asn].push(attack);
      return acc;
    }, {});
  };

  const items = Object.keys(groupedAttacks).map((asn, index) => {
    const columns = [
      {
        title: 'Prefixo',
        dataIndex: 'prefix',
        key: 'prefix',
        sorter: (a, b) => a.prefix.localeCompare(b.prefix),
      },
      {
        title: 'Método de Ataque',
        dataIndex: 'attack_method',
        key: 'attack_method',
      },
      {
        title: 'Protocolo',
        dataIndex: 'protocol',
        key: 'protocol',
      },
      {
        title: 'Porta Origem',
        dataIndex: 'source_port',
        key: 'source_port',
      },
      {
        title: 'Porta Destino',
        dataIndex: 'destination_port',
        key: 'destination_port',
      },
      {
        title: 'ICMP Type',
        dataIndex: 'icmp_type',
        key: 'icmp_type',
      },
      {
        title: 'ICMP CODE',
        dataIndex: 'icmp_code',
        key: 'icmp_code',
      },
      {
        title: 'Action',
        dataIndex: 'action',
        key: 'action',
        render: (_, record) => (
          <Select
            style={{ width: 120 }}
            onChange={(value) => handleActionChange(value, record.key)}
            placeholder={record.action}
          >
            <Select.Option value="Rate Limit">Rate Limit</Select.Option>
            <Select.Option value="Accept">Accept</Select.Option>
            <Select.Option value="Discard">Discard</Select.Option>
          </Select>
        ),
      },
      {
        title: 'Bandwidth',
        dataIndex: 'bandwidth',
        key: 'bandwidth',
        render: (_, record) => (
          <Input
            defaultValue={record.bandwidth}
            onChange={(e) => handleBandwidthChange(e.target.value, record.key)}
          />),
      },
      {
        title: 'Update',
        dataIndex: 'asn',
        key: 'asn',
        render: (_, record) => (
          <Button
            type="primary"
            onClick={() => handleUpdate(record.key, record.key)}
          >
            Update
          </Button>
        ),
      },
    ];

    // Prepare the dataSource for the Table
    const dataSource = groupedAttacks[asn].map((attack, attackIndex) => ({
      key: attack.id,
      prefix: attack.prefix,
      attack_method: attack.attack_method,
      protocol: attack.protocol,
      source_port: attack.source_port,
      destination_port: attack.destination_port,
      icmp_type: attack.icmp_type,
      icmp_code: attack.icmp_code,
      action: attack.action,
      bandwidth: attack.bandwidth,
      asn: attack.asn
      // Add other data fields as needed
    }));

    return {
      key: index.toString(),
      label: `AS${asn}`,
      children: (
        <div className="card my-3">
          <div className="card-body">
            <Table columns={columns} dataSource={dataSource} tableLayout='fixed' />
          </div>
        </div>
      ),
    };
  });

  useEffect(() => {
    handleSearchChange();
  }, [asnSearch, prefixSearch]);



  return (
    <Card>
      <Row gutter={12}>
        <Col span={12}>
          <Search
            placeholder="Pesquise pelo ASN"
            onSearch={handleSearchChange}
            onChange={(e) => setAsnSearch(e.target.value)}
            value={asnSearch}
          />
        </Col>
        <Col span={12}>
          <Search
            placeholder="Pesquisar por Prefixo"
            onSearch={handleSearchChange}
            onChange={(e) => setPrefixSearch(e.target.value)}
            value={prefixSearch}
          />
        </Col>
      </Row>

      <Divider />

      {!dataLoaded ? (
        <Progress percent={loadingProgress} status="active" />
      ) : (

        <Collapse accordion size='small' items={items} />
      )}
      {/* Render announcements */}
      <div id="announcements"></div>
    </Card>
  );
};

export default AntiGuerreiro;