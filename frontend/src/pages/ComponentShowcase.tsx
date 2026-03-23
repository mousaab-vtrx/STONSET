import React, { useState } from 'react'
import {
  Button,
  Card,
  CardHeader,
  CardBody,
  CardFooter,
  Input,
  Textarea,
  Select,
  FormGroup,
  Avatar,
  Badge,
  Alert,
  Modal,
  StatCard,
  Table,
} from '@/components/ui'

export const ComponentShowcase: React.FC = () => {
  const [isModalOpen, setIsModalOpen] = useState(false)

  return (
    <div className="max-w-7xl mx-auto px-4 py-8 space-y-8">
      {/* Header */}
      <div>
        <h1 className="heading-1 mb-2">Component Library</h1>
        <p className="text-muted">STONSET React UI Components</p>
      </div>

      {/* Buttons */}
      <section>
        <h2 className="heading-2 mb-6">Buttons</h2>
        <Card>
          <CardBody>
            <div className="flex flex-wrap gap-4">
              <Button variant="primary">Primary Button</Button>
              <Button variant="secondary">Secondary Button</Button>
              <Button variant="outline">Outline Button</Button>
              <Button variant="danger">Danger Button</Button>
              <Button variant="ghost">Ghost Button</Button>
              <Button variant="primary" size="sm">
                Small
              </Button>
              <Button variant="primary" size="lg">
                Large
              </Button>
              <Button variant="primary" loading>
                Loading
              </Button>
            </div>
          </CardBody>
        </Card>
      </section>

      {/* Cards */}
      <section>
        <h2 className="heading-2 mb-6">Cards</h2>
        <div className="grid md:grid-cols-2 gap-6">
          <Card>
            <CardHeader title="Card Title" subtitle="Card subtitle" action={<Badge variant="primary">New</Badge>} />
            <CardBody>
              <p>This is a card with header, body, and footer structure.</p>
            </CardBody>
            <CardFooter>
              <Button variant="outline" size="sm">
                Cancel
              </Button>
              <Button variant="primary" size="sm">
                Submit
              </Button>
            </CardFooter>
          </Card>

          <Card hoverable>
            <p className="font-semibold mb-2">Hoverable Card</p>
            <p className="text-muted text-sm">This card has a hover effect.</p>
          </Card>
        </div>
      </section>

      {/* Forms */}
      <section>
        <h2 className="heading-2 mb-6">Form Elements</h2>
        <Card>
          <CardBody className="max-w-md space-y-4">
            <FormGroup>
              <Input label="Email Address" type="email" placeholder="user@example.com" />
              <Input label="Full Name" placeholder="John Doe" error={false ? 'Name is required' : undefined} />
              <Textarea label="Message" placeholder="Enter your message..." rows={4} />
              <Select
                label="Choose Option"
                options={[
                  { value: '1', label: 'Option 1' },
                  { value: '2', label: 'Option 2' },
                  { value: '3', label: 'Option 3' },
                ]}
              />
            </FormGroup>
          </CardBody>
        </Card>
      </section>

      {/* Badges & Avatars */}
      <section>
        <h2 className="heading-2 mb-6">Badges & Avatars</h2>
        <Card>
          <CardBody>
            <div className="space-y-6">
              <div>
                <p className="font-semibold mb-3">Badges</p>
                <div className="flex flex-wrap gap-3">
                  <Badge variant="primary">Primary</Badge>
                  <Badge variant="success">Success</Badge>
                  <Badge variant="warning">Warning</Badge>
                  <Badge variant="error">Error</Badge>
                  <Badge variant="info">Info</Badge>
                </div>
              </div>
              <div>
                <p className="font-semibold mb-3">Avatars</p>
                <div className="flex items-center gap-4">
                  <Avatar initials="JD" size="sm" />
                  <Avatar initials="AB" size="md" />
                  <Avatar initials="CD" size="lg" />
                  <Avatar initials="EF" size="xl" />
                </div>
              </div>
            </div>
          </CardBody>
        </Card>
      </section>

      {/* Alerts */}
      <section>
        <h2 className="heading-2 mb-6">Alerts</h2>
        <Card>
          <CardBody className="space-y-3">
            <Alert variant="success" title="Success!" onClose={() => {}}>
              Your action completed successfully.
            </Alert>
            <Alert variant="warning" title="Warning" onClose={() => {}}>
              Please review before proceeding.
            </Alert>
            <Alert variant="error" title="Error" onClose={() => {}}>
              Something went wrong. Please try again.
            </Alert>
            <Alert variant="info" title="Info" onClose={() => {}}>
              This is informational content.
            </Alert>
          </CardBody>
        </Card>
      </section>

      {/* Stats */}
      <section>
        <h2 className="heading-2 mb-6">Statistics</h2>
        <div className="grid md:grid-cols-4 gap-6">
              <StatCard label="Total Users" value="12,543" icon="users" change={{ value: 12, trend: 'up' }} />
              <StatCard label="Active Reservations" value="847" icon="calendar" change={{ value: 5, trend: 'down' }} />
              <StatCard label="Rooms Available" value="24" icon="building" />
              <StatCard label="Completion Rate" value="94%" icon="check" change={{ value: 3, trend: 'up' }} />
        </div>
      </section>

      {/* Modal & Actions */}
      <section>
        <h2 className="heading-2 mb-6">Modal & Interactions</h2>
        <Card>
          <CardBody>
            <Button variant="primary" onClick={() => setIsModalOpen(true)}>
              Open Modal
            </Button>
          </CardBody>
        </Card>

        <Modal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} title="Example Modal" size="md"
          footer={
            <>
              <Button variant="outline" onClick={() => setIsModalOpen(false)}>
                Cancel
              </Button>
              <Button variant="primary">Confirm</Button>
            </>
          }
        >
          <p className="text-muted mb-4">This is an example modal. You can add any content here.</p>
          <Input placeholder="Enter value..." />
        </Modal>
      </section>

      {/* Table */}
      <section>
        <h2 className="heading-2 mb-6">Table</h2>
        <Card>
          <CardBody>
            <Table
              columns={[
                { key: 'name', label: 'Name' },
                { key: 'email', label: 'Email' },
                { key: 'role', label: 'Role' },
                {
                  key: 'status',
                  label: 'Status',
                  render: (value) => (
                    <Badge variant={value === 'active' ? 'success' : 'warning'}>
                      {value}
                    </Badge>
                  ),
                },
              ]}
              data={[
                { name: 'John Doe', email: 'john@example.com', role: 'Admin', status: 'active' },
                { name: 'Jane Smith', email: 'jane@example.com', role: 'User', status: 'active' },
                { name: 'Bob Johnson', email: 'bob@example.com', role: 'User', status: 'inactive' },
              ]}
            />
          </CardBody>
        </Card>
      </section>
    </div>
  )
}
