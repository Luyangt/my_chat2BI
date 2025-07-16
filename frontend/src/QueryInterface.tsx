import React, { useState, useEffect } from 'react';
import {
  Card,
  Input,
  Button,
  Table,
  Alert,
  Typography,
  Space,
  Spin,
  Tag,
  Select,
  Row,
  Col,
  Divider,
  Tooltip
} from 'antd';
import { SendOutlined, ReloadOutlined, QuestionCircleOutlined } from '@ant-design/icons';
import ApiService, { QueryResponse, SampleQuery } from './api';

const { Title, Text, Paragraph } = Typography;
const { TextArea } = Input;
const { Option } = Select;

const QueryInterface: React.FC = () => {
  const [question, setQuestion] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<QueryResponse | null>(null);
  const [sampleQueries, setSampleQueries] = useState<SampleQuery[]>([]);
  const [loadingSamples, setLoadingSamples] = useState(false);

  // 加载示例查询
  useEffect(() => {
    loadSampleQueries();
  }, []);

  const loadSampleQueries = async () => {
    setLoadingSamples(true);
    try {
      const response = await ApiService.getSampleQueries();
      setSampleQueries(response.sample_queries);
    } catch (error) {
      console.error('Failed to load sample queries:', error);
    } finally {
      setLoadingSamples(false);
    }
  };

  // 执行查询
  const handleQuery = async () => {
    if (!question.trim()) return;

    setLoading(true);
    setResult(null);

    try {
      const response = await ApiService.query({ question });
      setResult(response);
    } catch (error) {
      console.error('Query failed:', error);
      setResult({
        success: false,
        question,
        error: '查询失败，请检查网络连接或联系管理员'
      });
    } finally {
      setLoading(false);
    }
  };

  // 使用示例查询
  const handleSampleQuery = (sampleQuestion: string) => {
    setQuestion(sampleQuestion);
  };

  // 清空结果
  const handleClear = () => {
    setQuestion('');
    setResult(null);
  };

  // 准备表格数据
  const getTableData = () => {
    if (!result?.data || result.data.length === 0) return { columns: [], dataSource: [] };

    const firstRow = result.data[0];
    const columns = Object.keys(firstRow).map(key => ({
      title: key,
      dataIndex: key,
      key: key,
      width: 200,
      render: (value: any) => {
        if (value === null || value === undefined) return '-';
        if (typeof value === 'number') return value.toLocaleString();
        return String(value);
      }
    }));

    const dataSource = result.data.map((row, index) => ({
      ...row,
      key: index
    }));

    return { columns, dataSource };
  };

  const { columns, dataSource } = getTableData();

  return (
    <div style={{ padding: '24px', maxWidth: '1200px', margin: '0 auto' }}>
      <Title level={2} style={{ textAlign: 'center', marginBottom: '32px' }}>
        Chat2BI - 自然语言查询
      </Title>

      {/* 查询输入区域 */}
      <Card title="查询输入" style={{ marginBottom: '24px' }}>
        <Space direction="vertical" size="middle" style={{ width: '100%' }}>
          <div>
            <Text strong>请输入您的查询问题：</Text>
            <TextArea
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              placeholder="例如：总销售额是多少？"
              autoSize={{ minRows: 2, maxRows: 4 }}
              style={{ marginTop: '8px' }}
            />
          </div>
          
          <Row gutter={16}>
            <Col>
              <Button
                type="primary"
                icon={<SendOutlined />}
                onClick={handleQuery}
                loading={loading}
                disabled={!question.trim()}
              >
                查询
              </Button>
            </Col>
            <Col>
              <Button
                icon={<ReloadOutlined />}
                onClick={handleClear}
              >
                清空
              </Button>
            </Col>
          </Row>
        </Space>
      </Card>

      {/* 示例查询 */}
      <Card 
        title={
          <Space>
            <span>示例查询</span>
            <Tooltip title="点击示例查询可以快速填入查询框">
              <QuestionCircleOutlined />
            </Tooltip>
          </Space>
        }
        style={{ marginBottom: '24px' }}
      >
        {loadingSamples ? (
          <Spin />
        ) : (
          <Row gutter={[16, 16]}>
            {sampleQueries.map((sample, index) => (
              <Col xs={24} sm={12} md={8} lg={6} key={index}>
                <Card 
                  size="small" 
                  hoverable
                  onClick={() => handleSampleQuery(sample.question)}
                  style={{ cursor: 'pointer' }}
                >
                  <Text strong>{sample.question}</Text>
                  <br />
                  <Text type="secondary" style={{ fontSize: '12px' }}>
                    {sample.description}
                  </Text>
                </Card>
              </Col>
            ))}
          </Row>
        )}
      </Card>

      {/* 查询结果 */}
      {result && (
        <Card title="查询结果" style={{ marginBottom: '24px' }}>
          <Space direction="vertical" size="middle" style={{ width: '100%' }}>
            {/* 查询信息 */}
            <div>
              <Text strong>查询问题：</Text>
              <Text>{result.question}</Text>
            </div>

            {result.success ? (
              <>
                {/* 执行信息 */}
                <Row gutter={16}>
                  <Col>
                    <Tag color="green">查询成功</Tag>
                  </Col>
                  <Col>
                    <Text type="secondary">
                      执行时间: {result.execution_time?.toFixed(3)}秒
                    </Text>
                  </Col>
                  <Col>
                    <Text type="secondary">
                      结果数量: {result.count} 条
                    </Text>
                  </Col>
                </Row>

                {/* SQL语句 */}
                {result.sql && (
                  <div>
                    <Text strong>生成的SQL：</Text>
                    <Paragraph
                      code
                      copyable
                      style={{ 
                        background: '#f6f8fa', 
                        padding: '12px', 
                        borderRadius: '6px',
                        margin: '8px 0'
                      }}
                    >
                      {result.sql}
                    </Paragraph>
                  </div>
                )}

                {/* 结果表格 */}
                {result.data && result.data.length > 0 ? (
                  <div>
                    <Divider />
                    <Text strong>查询结果：</Text>
                    <Table
                      columns={columns}
                      dataSource={dataSource}
                      size="small"
                      scroll={{ x: 'max-content' }}
                      pagination={{
                        pageSize: 10,
                        showSizeChanger: true,
                        showQuickJumper: true,
                        showTotal: (total, range) => 
                          `第 ${range[0]}-${range[1]} 条，共 ${total} 条`
                      }}
                      style={{ marginTop: '16px' }}
                    />
                  </div>
                ) : (
                  <Alert
                    message="无查询结果"
                    description="查询执行成功，但没有返回数据"
                    type="info"
                    showIcon
                  />
                )}
              </>
            ) : (
              <Alert
                message="查询失败"
                description={result.error}
                type="error"
                showIcon
              />
            )}
          </Space>
        </Card>
      )}
    </div>
  );
};

export default QueryInterface; 