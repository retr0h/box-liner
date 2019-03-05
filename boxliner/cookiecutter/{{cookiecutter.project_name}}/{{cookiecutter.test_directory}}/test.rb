describe group('root') do
  it { should exist }
  its('gid') { should eq 0 }
end
